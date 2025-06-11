from datetime import date
from typing import Optional
from pydantic import BaseModel
from agents import Agent, ModelSettings

from llm_agents.search.tools.deep_dive_tool import deep_dive_tool

PROMPT = (
"""
You are an expert table generator agent. Your sole purpose is to convert provided data into a CSV (Comma Separated Values) formatted string.

Your output must adhere to the following rules:

- Strict CSV Format: The data should be organized with comma-separated values.
- Header Row: Always include a header row as the first line of the CSV.
- No Extra Characters: Do not include any introductory or concluding text, only the CSV data itself.
- No Exceptions: Deviations from this format are not permitted.
"""
)

class CSVResult(BaseModel):
    csv_file: str
    """Strict CSV format that is ready to generate a CSV file."""
    
csv_maker_agent = Agent(
    name="CSV Generator Agent",
    instructions=PROMPT,
    model="gpt-4o-mini",
    output_type=CSVResult,
)