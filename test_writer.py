from agents import Runner
from llm_agents.campaign.agent import campaign_agent, CampaignsList
from llm_agents.search.tools.deep_dive_tool import deep_dive_tool
from _agents.writer import writer_agent, ReportSectionData

data_input = ""

with open('context.txt', 'r') as file:
    for line in file:
        print(line.strip())
        data_input += line.strip() + " "

async def main():
    result = await Runner().run(
        writer_agent,
        input=f"""
        Given this data: {data_input}. \n\n
        Generate a detailed comprehensive promotion campaign analysis report from the given data.
        The report must have table visualization for data to list all promotion campaigns from Nike and Adidas in April 2025 for each country.
        The report should be structured with the following sections:
        1. **Introduction**: Provide a concise overview of the report's purpose and scope.
        2. **Promotion Campaigns Analysis**: Analyze the promotion campaigns from Nike and Adidas in April 2025, including key metrics, trends, and insights.
        3. **Country-Specific Campaigns**: List all promotion campaigns from Nike and Adidas in April 2025 for each country, including details such as campaign name, company name, start date, end date, mechanic, offerings, and URL.
        4. **Conclusion**: Summarize the key findings and insights from the analysis.
        Ensure the report is well-structured, with appropriate headings and subheadings, and includes markdown tables for data visualization.
        The report should be written in a formal, professional, and analytical tone, using markdown formatting for clarity and emphasis.
        """
    )
    report  = result.final_output_as(ReportSectionData)
    print(report.markdown_report)
    
    with open("report-test.md", "w", encoding="utf-8") as file:
        file.write(report.markdown_report)
    
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())