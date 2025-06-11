from enum import Enum
from pydantic import BaseModel
from agents import Agent

PROMPT = (
"""
You are a Country Codes detector that identifies a list of country names and ISO 3166-1 alpha-2 country codes from a given region.
"""
)

class CountryCode(BaseModel):
    code: str
    """ISO 3166-1 alpha-2 country code (e.g., 'th' for Thailand, 'sg' for Singapore)."""
    
    country_name: str
    """The name of the country corresponding to the ISO code (e.g., 'Thailand', 'Singapore')."""

class CountriesList(BaseModel):
    countries: list[CountryCode]
    """A list of country codes and names."""
    
countries_detector_agent = Agent(
    name="Countries Detector",
    instructions=PROMPT,
    model="gpt-4o-mini",
    output_type=CountriesList,
)