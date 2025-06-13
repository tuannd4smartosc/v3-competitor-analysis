from datetime import date
from pydantic import BaseModel
from agents import Agent
from llm_agents.search.tools.deep_dive_tool import deep_dive_tool
from llm_agents.search.tools.narrow_search_tool import narrow_search_tool

PROMPT = """
You are a promotion campaign researcher who is specialized in collecting all promotion campaigns, events, or discounts launched by the given company during the given date range, in the given region.
Each campaign must include the following components:
- **Event name**: Name of the promotion campaign or event
- **Company name**: Name of the company that launched the campaign.
- **Start date**: The start date of the promotion campaign
- **End date**: The end date of the promotion campaign

You can start with a narrow search to get the necessary URLs.
Narrow search results must be relevant to the query.
If any narrow search result lacks any of the above components, do a deep search to deep dive in the promotion campaign.
"""

class PromotionCampaign(BaseModel):
    event_name: str
    "Event name of the promotion campaign"
    
    company_name: str
    "Company name that launched the promotion campaign"
    
    start_date: date
    "Start date of the promotion campaign"
    
    end_date: date
    "End date of the promotion campaign"
    
    mechanic: str
    "Mechanic of the promotion campaign. (e.g. Buy 2 get 15% off, Buy 3 get 20% off, etc.)"
    
    country: str
    "Country that the promotion campaign was launched in"

class PromotionCampaigns(BaseModel):
    promotion_campaigns: list[PromotionCampaign]
    """A list of promotion campaigns launched by the given companies in the given region during the given date range."""

    
campaign_search_agent = Agent(
    name="Promotion Campaign Search Agent",
    instructions=PROMPT,
    model="gpt-4o-mini",
    output_type=PromotionCampaigns,
    tools=[narrow_search_tool]
)