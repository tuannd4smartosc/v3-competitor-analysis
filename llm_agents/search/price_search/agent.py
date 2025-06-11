from pydantic import BaseModel
from agents import Agent
from llm_agents.search.tools.shopping_tool import shopping_search_tool

PROMPT = """
You are Search Agent, an expert research assistant focused on competitive intelligence. Your task is to conduct reliable and focused web searches to support competitor analysis. Return only factual, structured, and well-sourced information.

For each result:
- Prioritize structured data, comparative metrics, market share statistics, pricing models, product features, growth indicators, or user sentiment summaries.
- Avoid opinions, vague generalizations, or purely promotional content unless substantiated by reliable data.
- Ensure data credibility by preferring official company reports, trusted media, analyst reports, industry publications, or verified third-party aggregators.
- Include the exact URL to the source of the data.
- Use the `need_deep_dive` flag as `True` if the result appears valuable but lacks full context, precision, or needs further analysis.

Translate all search results into English if they are in another language, ensuring the information remains accurate and relevant.
Respond with a list of `SearchResultsItem` objects inside a `SearchResult`. Focus on quality over quantity—aim for high-value, informative entries.
"""

class SearchResultsItem(BaseModel):
    search_result: str
    """The result of the search query, which should be a structured dataset, reliable facts or a detailed statistic relevant to the competitor analysis."""
    
    has_promotion_campaign: bool
    """Indicates whether the search result contains information about a promotion campaign, marketing event, or a product launch."""
    
    relativity_score: float
    """A score indicating the relevance of the search result to the query, on a scale from 0.0 to 1.0."""
    
    url: str
    """URL of the source where the search result was found."""
    
    need_deep_dive: bool
    """Indicates whether the search result requires further analysis or deep dive to extract more detailed information. If the result doesn't have enough information for all the fields: campaign_name, company_name, start_date, end_date, mechanic, offering, country, summary, url, then this should be set to True."""

class SearchResult(BaseModel):
    search_results: list[SearchResultsItem]
    """A list of search results, each containing relevant data and references."""
    
class SearchMetadata(BaseModel):
    query: str
    """The search query used to perform the search."""
    
    country_code: str
    """ISO 3166-1 alpha-2 country code to filter the search results by country (e.g., 'th', 'sg', 'vn', 'id')."""
    
    search_type: str
    """Type of search required. The type must be either web_search, or news_search."""

class SearchResultWithMetadata(BaseModel):
    search_result_item: SearchResultsItem
    """The search result item containing structured data and references."""
    
    metadata: SearchMetadata
    """Metadata about the search, such as the query, date range, country code, and search type."""
    
price_research_agent = Agent(
    name="Price Research Agent",
    instructions=PROMPT,
    model="gpt-4o-mini",
    output_type=SearchResult,
    tools=[shopping_search_tool]
)