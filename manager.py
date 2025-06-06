import asyncio
import time
import uuid

from agents import Runner, custom_span, gen_trace_id, trace
from openai import BaseModel
from _agents.planner import WebSearchItem, WebSearchPlan, planner_agent
from _agents.search import search_agent
from _agents.writer import ReportData, writer_agent
from _agents.chart import chart_agent
from crews.price_comparison import generate_price_analysis_user_query
from crews.promotion_campaigns import generate_promotion_campaign_user_query
from crews.traffic_revenue import generate_traffic_revenue_query
from file_handler import export_md

class SectionRequest(BaseModel):
    topic: str
    user_prompt: str

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
                topic="Promotion campaigns",
                user_prompt=generate_promotion_campaign_user_query(
                    *params
                ),
            ),
            SectionRequest(
                topic="Price analysis",
                user_prompt=generate_price_analysis_user_query(
                    *params
                ),
            ),
            SectionRequest(
                topic="Traffic & Revenue",
                user_prompt=generate_traffic_revenue_query(
                    *params
                ),
            ),
        ]
        tasks = [self.generate_section(user_prompt) for user_prompt in section_requests]
        print("tasks",tasks)
        section_outputs = await asyncio.gather(*tasks)
        section_markdowns = [section.markdown_report for section in section_outputs]
        final_output = "\n\n".join(section_markdowns)
        print("final_output", final_output)
        export_md(final_output, "test-report.md")
        return section_outputs
        
        
    async def generate_section(self, query: str):
        trace_id = gen_trace_id()
        with trace("Research trace", trace_id=trace_id):
            try:
                search_plan = await self._plan_searches(query)
                print("search_plan:", search_plan)

                search_results = await self._perform_searches(search_plan)
                print("search_results completed!")

                section = await self._write_section(query, search_results)
                return section
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
        print(">>>>>>> Section:", result)
        return result.final_output_as(ReportData)
    
    async def _generate_charts(self, search_results: list[str]) -> None:
        input = f"Search results: {search_results} \nGenerate a pie chart of the market share of the provided companies."
        result = await Runner.run(
            chart_agent,
            input,
        )
        print(f"Generated chart: {result.final_output}")
        return result.final_output