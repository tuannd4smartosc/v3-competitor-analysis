from pydantic import BaseModel

from agents import Agent

PROMPT = (
    "You are a highly capable research assistant tasked with helping to answer complex queries. "
    "Given a query, your goal is to come up with the most detailed and comprehensive set of web searches "
    "that will best help answer the query. Consider breaking down the query into its main components, including "
    "keywords, related concepts, and the underlying intent. Make sure to include various types of search terms "
    "(e.g., factual questions, exploratory searches, related terms, synonyms, and relevant subtopics). "
    "Additionally, consider refining the search terms to ensure high-quality, focused results. "
    "Your output should be a list of searches (15 searches minimum, encourage to search more if necessary) that can cover different angles of the query, addressing any nuances "
    "and ensuring comprehensive coverage of the topic."
)


class WebSearchItem(BaseModel):
    reason: str
    "Your reasoning for why this search is important to the query."

    query: str
    "The search term to use for the web search."


class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem]
    """A list of web searches to perform to best answer the query."""


planner_agent = Agent(
    name="PlannerAgent",
    instructions=PROMPT,
    model="o1",
    output_type=WebSearchPlan,
)