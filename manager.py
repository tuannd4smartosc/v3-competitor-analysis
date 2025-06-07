import asyncio
import time
import uuid

from agents import Runner, custom_span, gen_trace_id, trace
from openai import BaseModel
from _agents.planner import WebSearchItem, WebSearchPlan, planner_agent
from _agents.search import search_agent
from _agents.writer import ReportData, writer_agent
from _agents.chart import ChartOutput, chart_agent
from crews.price_comparison import generate_price_analysis_user_query
from crews.promotion_campaigns import generate_promotion_campaign_user_query
from crews.traffic_revenue import generate_traffic_revenue_query
from file_handler import export_md
from utils import get_first_temp_filename

topics = {
    "promotion_campaigns": "Promotion campaigns",
    "pricing_analysis": "Price analysis",
    "traffic_revenue": "Traffic & Revenue"
}

class SectionRequest(BaseModel):
    topic: str
    user_prompt: str

class SectionOutputData(BaseModel):
    markdown_text: str
    chart_data: ChartOutput | None

class AiManager:
    def __init__(self, company_name, competitors_names, date_range, region):
        self.company_name = company_name
        self.competitors_names = competitors_names
        self.date_range = date_range
        self.region = region
        
    async def run_crews(self):
        params = [self.company_name, self.competitors_names, self.date_range, self.region]
        section_requests = [
            SectionRequest(
                topic=topics["promotion_campaigns"],
                user_prompt=generate_promotion_campaign_user_query(
                    *params
                ),
            ),
            SectionRequest(
                topic=topics["pricing_analysis"],
                user_prompt=generate_price_analysis_user_query(
                    *params
                ),
            ),
            SectionRequest(
                topic=topics["traffic_revenue"],
                user_prompt=generate_traffic_revenue_query(
                    *params
                ),
            ),
        ]
        tasks = [self.generate_section(section_req.topic, section_req.user_prompt) for section_req in section_requests]
        print("tasks",tasks)
        section_outputs = await asyncio.gather(*tasks)
        full_report = ""
        for section in section_outputs:
            full_report += "\n\n" + section.markdown_text
            if(section.chart_data):
                chart_filename = get_first_temp_filename("temp")
                print("chart_filename", chart_filename)
                full_report += "\n\n" + f"![Chart](temp/{chart_filename})" + "\n" + f"*{section.chart_data.chart_description}*"
        print("<<<<<<<< full_report", full_report)
        export_md(full_report, "test-report.md")
        return section_outputs
        
        
    async def generate_section(self, topic: str, query: str) -> SectionOutputData:
        trace_id = gen_trace_id()
        with trace("Research trace", trace_id=trace_id):
            try:
                search_plan = await self._plan_searches(query)
                print("search_plan:", search_plan)

                search_results = await self._perform_searches(search_plan)
                print("search_results completed!")

                section = await self._write_section(query, search_results)
                
                chart_data = None
                print("topic", topic, topics["pricing_analysis"], topic == topics["pricing_analysis"])
                if(topic == topics["pricing_analysis"]):
                    print(">>> Creating chart", topic)
                    chart_data = await self._generate_charts(search_results)
                    print(">>>>>>>>>. chart_data", chart_data)
                
                
                return SectionOutputData(
                    markdown_text=section.markdown_report,
                    chart_data=chart_data
                )
            except Exception as e:
                print(f"generate_section failed for query={query}: {e}")
                return None
        
    def generate_report_id(self):
        return f"report-{self.competitors_name}-{self.region}-{self.date_range}-{uuid.uuid4().hex}"
    
    async def _plan_searches(self, query: str) -> WebSearchPlan:
        result = await Runner.run(
            planner_agent,
            f"Query: {query}",
        )
        return result.final_output_as(WebSearchPlan)

    async def _perform_searches(self, search_plan: WebSearchPlan) -> list[str]:
        with custom_span("Search the web"):
            num_completed = 0
            tasks = [asyncio.create_task(self._search(item)) for item in search_plan.searches]
            results = []
            for task in asyncio.as_completed(tasks):
                result = await task
                if result is not None:
                    results.append(result)
                num_completed += 1
            return results

    async def _search(self, item: WebSearchItem) -> str | None:
        input = f"Search term: {item.query}\nReason for searching: {item.reason}"
        try:
            result = await Runner.run(
                search_agent,
                input,
            )
            return str(result.final_output)
        except Exception:
            return None

    async def _write_section(self, query: str, search_results: list[str]) -> ReportData:
        input = f"Original query: {query}\nSummarized search results: {search_results}"
        result = await Runner.run(
            writer_agent,
            input,
        )
        return result.final_output_as(ReportData)
    
    async def _generate_charts(self, search_results: list[str]) -> ChartOutput:
        input = f"""
        Search results:
        {search_results}

        Based on the provided search results, generate a heat map that visualizes and compares the discount rates of the top 5 products from each brand. For each product, use the following attributes:

        - Product name
        - Brand
        - Original price
        - Discounted price

        Calculate the discount rate as a percentage:
            - Discount Rate = (Original Price - Discounted Price) / Original Price × 100%

        Display one heat map where each cell represents a product, grouped by brand, with color intensity indicating the discount rate. Use clear labeling to identify products and their respective brands.
        """
        result = await Runner.run(
            chart_agent,
            input,
        )
        print(f"Generated chart: {result.final_output}")
        return result.final_output