from datetime import date
from typing import Optional
from pydantic import BaseModel
from agents import Agent, ModelSettings

from llm_agents.search.tools.deep_dive_tool import deep_dive_tool

PROMPT = (
"""
You are a researcher expert in promotion campaigns and advertisements.
Your task is to identify and list all *major and verifiable* promotion campaigns run by the given company using deep web search tools.
Focus on campaigns with clear start and end dates, and distinct mechanics.
Once you have found at least 3-5 distinct campaigns, or if further deep dives yield diminishing returns (i.e., no new, significant campaigns are found after several searches), synthesize the information and output the results.
If you cannot find any campaigns, state that clearly.

Your output should be a list of promotion campaigns with the following details:
- Campaign Name: The name of the promotion campaign.
- Company Name: The name of the company running the campaign.
- Start Date: The start date of the campaign. (Estimate if only month/year is available)
- End Date: The end date of the campaign. (Estimate if only month/year is available, or indicate "ongoing" if no end date)
- Mechanic: The promotional mechanic used in the campaign, such as '40% discount', 'buy one get one free', 'loyalty program', 'contest', 'giveaway', 'limited-time offer', etc.
- Country: The country where the campaign is being run.
- Summary: A brief summary of the campaign, including its objectives and key messages.
- URL: The URL that was used to find the campaign details.

Ensure that the information is accurate, well-structured, and relevant to the promotion campaigns.
Translate the campaign details into English if they are in another language.
"""
)

class Campaign(BaseModel):
    campaign_name: str
    """The name of the promotion campaign."""
    
    company_name: str
    """The name of the company running the campaign."""
    
    start_date: date
    """The start date of the campaign."""
    
    end_date: date
    """The end date of the campaign."""
    
    mechanic: str
    """The promotional mechanic used in the campaign, such as '30% discount', 'buy one get one free', etc."""
    
    country: str
    """The country where the campaign is being run."""
    
    summary: str
    """A brief summary of the campaign, including its objectives and key messages."""
    
    url: str
    """The URL that was used to find the campaign details."""
    
    offering: Optional[str] = None
    """Optional field for additional information about the campaign offering. For exapmle, '40% off on selected items'."""
    
    class Config:  
        extra = "forbid" 

class CampaignsList(BaseModel):
    campaigns: list[Campaign]
    """A list of promotion campaigns."""
    
campaign_agent = Agent(
    name="Promotion Campaigns Agent",
    instructions=PROMPT,
    model="gpt-4o-mini",
    output_type=CampaignsList,
    tools=[deep_dive_tool],
    model_settings=ModelSettings(tool_choice="required"),
    
)