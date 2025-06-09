import asyncio
import itertools
import os
import uuid

from agents import Runner, custom_span, gen_trace_id, trace
from openai import BaseModel
from _agents.planner import WebSearchItem, WebSearchPlan, planner_agent
from _agents.search import search_agent, SearchResult, APAWebReference
from _agents.writer import ReportSectionData, writer_agent
from _agents.chart import ChartListOutput, chart_agent
from config import REPORT_DIR
from crews.price_comparison import generate_price_analysis_user_query
from crews.promotion_campaigns import generate_promotion_campaign_user_query
from crews.traffic_revenue import generate_traffic_revenue_query
from utils import generate_citation_markdown, markdown_to_pdf, export_md

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
    chart_data: ChartListOutput | None
    section_title: str
    reference_list: list[APAWebReference]
    
class FinalOutputData(BaseModel):
    full_report: str
    file_name: str

class AiManager:
    def __init__(self, company_name, competitors_names, date_range, region, printer):
        self.company_name = company_name
        self.competitors_names = competitors_names
        self.date_range = date_range
        self.region = region
        self.printer = printer
        
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
        section_outputs = await asyncio.gather(*tasks)
        report_title = f"Competitor Analysis Report: {self.company_name} vs {self.competitors_names} in ({self.region}, {self.date_range})"
        full_report = ""
        full_report += f"# {report_title}\n\n"
        references = []
        for section in section_outputs:
            full_report += "\n\n" + f"## {section.section_title}" + "\n\n" + section.markdown_text
            if(section.chart_data):
                for chart in section.chart_data.charts:
                    print("chart", chart)
                    chart_filename = chart.output_file_path if chart.output_file_path else "https://media.istockphoto.com/id/1409329028/vector/no-picture-available-placeholder-thumbnail-icon-illustration-design.jpg?s=612x612&w=0&k=20&c=_zOuJu755g2eEUioiOUdz_mHKJQJn-tDgIAhQzyeKUQ="
                    print("chart_filename", chart_filename)
                    full_report += "\n\n" + f"![Chart]({chart_filename})" + "\n" + f"*{chart.chart_description}*"
            references = references + section.reference_list
        citation_markdown = generate_citation_markdown(references)
        full_report += "\n\n" + "## References" + "\n\n" + citation_markdown
        file_name = f"{self.generate_report_id()}.md"
        export_md(full_report, file_name)
        pdf_path = os.path.join(REPORT_DIR, file_name.replace(".md", ".pdf"))
        markdown_to_pdf(full_report, pdf_path)
        return FinalOutputData(
            full_report=full_report,
            file_name=file_name
        )
        
        
    async def generate_section(self, topic: str, query: str) -> SectionOutputData:
        trace_id = gen_trace_id()
        with trace("Research trace", trace_id=trace_id):
            try:
                self.printer.update_item("writing", f"Thinking about section: {topic}", is_done=False)
                search_plan = await self._plan_searches(query)
                print("search_plan:", search_plan)

                search_results = await self._perform_searches(search_plan)
                print("search_results completed!")
                
                search_results_texts = [item.search_result for item in search_results]
                reference_list = list(itertools.chain.from_iterable([item.reference_list for item in search_results]))
                self.printer.update_item("writing", f"Starting writing section: {topic}", is_done=False)
                section = await self._write_section(query, search_results_texts)
                chart_data = None
                print("topic", topic, topics["pricing_analysis"], topic == topics["pricing_analysis"])
                if(topic == topics["pricing_analysis"]):
                    print(">>> Creating chart", topic)
                    chart_data = await self._generate_charts(section.markdown_report)
                    print(">>>>>>>>>. chart_data", chart_data)
                self.printer.update_item("writing", f"Finished writing section: {topic}", is_done=False)
                
                return SectionOutputData(
                    markdown_text=section.markdown_report,
                    chart_data=chart_data,
                    section_title=section.section_title,
                    reference_list=reference_list
                )
            except Exception as e:
                print(f"generate_section failed for query={query}: {e}")
                return None
        
    def generate_report_id(self):
        return f"report-{self.competitors_names}-{self.region}-{self.date_range}-{uuid.uuid4().hex}"
    
    async def _plan_searches(self, query: str) -> WebSearchPlan:
        result = await Runner.run(
            planner_agent,
            f"Query: {query}",
        )
        return result.final_output_as(WebSearchPlan)

    async def _perform_searches(self, search_plan: WebSearchPlan) -> list[SearchResult]:
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

    async def _search(self, item: WebSearchItem) -> SearchResult | None:
        input = f"Search term: {item.query}\nReason for searching: {item.reason}"
        try:
            result = await Runner.run(
                search_agent,
                input,
            )
            return result.final_output_as(SearchResult)
        except Exception:
            return None

    async def _write_section(self, query: str, search_results: list[str]) -> ReportSectionData:
        print("search_results", search_results)
        input = f"Original query: {query}\nSummarized search results: {search_results}"
        result = await Runner.run(
            writer_agent,
            input,
        )
        return result.final_output_as(ReportSectionData)
    
    async def _generate_charts(self, data_context: str) -> ChartListOutput:
        input = f"""
        Provided data context for chart generation:
        {data_context}

        From the search results above, generate multiple heapmaps, one separate heatmap for each country found in the provided data above. 
        Each heatmap should display the discount rates of products grouped by their country of origin.
        The heatmap should have product names or brands on one axis and their respective discount percentages on the other.
        For each product, use the following attributes:

        - Product name
        - Brand
        - Original price
        - Discounted price
        - Location (country of origin)

        Calculate the discount rate as a percentage:
            - Discount Rate = (Original Price - Discounted Price) / Original Price × 100%

        Display one heat map where each cell represents a product, grouped by brand, with color intensity indicating the discount rate. Use clear labeling to identify products and their respective brands.
        """
            
        result = await Runner.run(
            chart_agent,
            input,
        )
        print(f"Generated chart: {result.final_output}")
        return result.final_output_as(ChartListOutput)