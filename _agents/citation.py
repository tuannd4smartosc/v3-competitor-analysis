# Agent used to synthesize a final report from the individual summaries.
from pydantic import BaseModel

from agents import Agent

PROMPT = (
 """
 
 """
)

citation_agent = Agent(
    name="APA Citation Agent",
    instructions=PROMPT,
    model="gpt-4o-mini",
    output_type=str,
)