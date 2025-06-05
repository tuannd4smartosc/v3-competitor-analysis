from __future__ import annotations

import asyncio
import time

from agents import Runner, custom_span, gen_trace_id, trace

from _agents.chart_agent import chart_agent
from _agents.planner_agent import WebSearchItem, WebSearchPlan, planner_agent
from _agents.search_agent import search_agent
from _agents.writer_agent import ReportData, writer_agent
from printer import Printer
from file_handler import export_md
from datetime import datetime
from utils import markdown_to_pdf
import os
from email_sender import send_email_with_attachment
from config import REPORT_DIR

class ResearchManager:
    def __init__(self, id, printer):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.printer = printer
        self.file_name = f"{id}-{timestamp}.md"
        self.id = id

    async def run(self, query: str) -> None:
        trace_id = gen_trace_id()
        with trace("Research trace", trace_id=trace_id):
            self.printer.update_item(
                "trace_id",
                f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}",
                is_done=True,
                hide_checkmark=True,
            )

            self.printer.update_item(
                "starting",
                "\nStarting research...",
                is_done=True,
                hide_checkmark=True,
            )
            search_plan = await self._plan_searches(query)
            search_results = await self._perform_searches(search_plan)
            report = await self._write_report(query, search_results)
            if search_plan.need_chart:
                chart_output_file = await self._generate_charts(search_results)
            
            print("report",report)
            # final_report = f"Report summary\n\n{report.short_summary}"
            # self.printer.update_item("final_report", final_report, is_done=True)

            self.printer.end()

        print("\n\n=====REPORT=====\n\n")
        # print(f"Report: {report.markdown_report}")
        print("\n\n=====FOLLOW UP QUESTIONS=====\n\n")
        # follow_up_questions = "\n".join(report.follow_up_questions)
        # print(f"\n\nFollow up questions: {follow_up_questions}")
        # export_md(report.markdown_report, self.file_name)
        print("\n\nEXPORTED REPORT MD SUCCESSFULLY!")
        pdf_path = os.path.join(REPORT_DIR, self.file_name.replace(".md", ".pdf"))
        # markdown_to_pdf(report.markdown_report, pdf_path)
        print("\nEXPORTED REPORT PDF SUCCESSFULLY!")
        subject = f"Competitor Analysis Report: {self.id}"
        body = "This is a test email with an attachment sent via Mailtrap."
        from_email = "sender@example.com"  
        to_email = "recipient@example.com"  
        file_paths = [pdf_path]
        print("\n\n START SENDING EMAIL!")
        # send_email_with_attachment(subject, body, from_email, to_email, report.markdown_report, file_paths)
        print("\n\n SENT EMAIL SUCCESSFULLY!")
        
    async def _plan_searches(self, query: str) -> WebSearchPlan:
        self.printer.update_item("planning", "Planning searches...")
        result = await Runner.run(
            planner_agent,
            f"Query: {query}",
        )
        self.printer.update_item(
            "planning",
            f"Will perform {len(result.final_output.searches)} searches",
            is_done=True,
        )
        return result.final_output_as(WebSearchPlan)

    async def _perform_searches(self, search_plan: WebSearchPlan) -> list[str]:
        with custom_span("Search the web"):
            self.printer.update_item("searching", "Searching...")
            num_completed = 0
            tasks = [asyncio.create_task(self._search(item)) for item in search_plan.searches]
            results = []
            for task in asyncio.as_completed(tasks):
                result = await task
                if result is not None:
                    results.append(result)
                num_completed += 1
                self.printer.update_item(
                    "searching", f"Searching... {num_completed}/{len(tasks)} completed"
                )
            self.printer.mark_item_done("searching")
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

    async def _write_report(self, query: str, search_results: list[str]) -> ReportData:
        self.printer.update_item("writing", "\nThinking about report...\nThis could take a few minutes.\n")
        input = f"Original query: {query}\nSummarized search results: {search_results}"
        result = Runner.run_streamed(
            writer_agent,
            input,
        )
        update_messages = [
            "\nThinking about report...\nThis could take a few minutes.",
            "\nPlanning report structure...",
            "\nWriting outline...",
            "\nCreating sections...",
            "\nCleaning up formatting...",
            "\nFinalizing report...",
            "\nFinishing report...\nThis could take a few minutes.",
        ]

        last_update = time.time()
        next_message = 0
        async for _ in result.stream_events():
            if time.time() - last_update > 5 and next_message < len(update_messages):
                self.printer.update_item("writing", update_messages[next_message])
                next_message += 1
                last_update = time.time()

        self.printer.mark_item_done("writing")
        return result.final_output_as(ReportData)
    
    async def _generate_charts(self, search_results: list[str]) -> None:
        self.printer.update_item("generating_charts", "Generating charts...")
        input = f"Search results: {search_results} \nGenerate a pie chart of the market share of the provided companies."
        result = await Runner.run(
            chart_agent,
            input,
        )
        print(f"Generated chart: {result.final_output}")
        return result.final_output
        