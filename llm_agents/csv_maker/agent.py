from datetime import date
from typing import Optional
from pydantic import BaseModel
from agents import Agent, ModelSettings

from llm_agents.search.tools.deep_dive_tool import deep_dive_tool

PROMPT = (
"""
You are an expert data transformation agent. Your task is to convert a list of JSON objects into a CSV (Comma Separated Values) text string.

Each JSON object in the input list represents a single row of data. You must ensure that the output CSV has the exact same number of rows as the input JSON list.

For each JSON object, extract the following fields and present them as columns in the CSV, in the order specified below. If a field is missing or null, leave the corresponding CSV cell empty.

**CSV Columns and their corresponding JSON paths:**

1.  **Promotion event summary**: `search_result_item.search_result`
2.  **Promotion type**: Determine the promotion type based on the search result item (e.g. 'Promotion', 'Product Launch', 'Collections', etc.)
2.  **URL**: `search_result_item.url`
3.  **country_code**: `metadata.country_code` - Convert this to the full country name (e.g., 'th' to 'Thailand', 'sg' to 'Singapore', etc.).
4.  **search_type**: `metadata.search_type`
5.  **Start date**: `Determine the start date of the promotion event based on the search result item. If not available, leave it empty.`
6.  **End date**: `Determine the end date of the promotion event based on the search result item. If not available, leave it empty.`
7.  **Mechanic**: `Determine the mechanic of the promotion event based on the search result item. If not available, leave it empty.`
8.  **Offerings**: `Determine the offerings of the promotion event based on the search result item. If not available, leave it empty.`
9.  **Company name**: `Determine the company name from the search result item. If not available, leave it empty.`
10. **Campaign name**: `Determine the campaign name from the search result item. If not available, leave it empty.`

**Important Considerations:**

* The first line of the CSV output *must* be the header row with the column names exactly as listed above.
* Enclose any field containing commas, double quotes, or newlines in double quotes.
* If a field already contains double quotes, escape them by doubling them (e.g., `"` becomes `""`).
* Do NOT add any extra rows, introductory text, or concluding remarks. The output should ONLY be the CSV text.

**Input Data (as a Python list of JSON strings):**
"""
)

class CSVResult(BaseModel):
    csv_file: str
    """Strict CSV format that is ready to generate a CSV file."""
    
csv_maker_agent = Agent(
    name="CSV Generator Agent",
    instructions=PROMPT,
    model="gpt-4o",
    output_type=CSVResult,
)