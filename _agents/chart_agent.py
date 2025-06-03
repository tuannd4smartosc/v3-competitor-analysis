from pydantic import BaseModel

from agents import Agent, FunctionTool

from tools.market_share_chart_tool import market_share_chart_tool

PROMPT = (
"""
You are a market research assistant specializing in generating visualizations for market share data in the footwear industry.
"""
)


class WebSearchItem(BaseModel):
    reason: str
    "Your reasoning for why this search is important to the query."

    query: str
    "The search term to use for the web search."


chart_agent = Agent(
    name="ChartAgent",
    instructions=PROMPT,
    model="gpt-4o-mini",
    tools=[market_share_chart_tool],
    output_type=str,
)