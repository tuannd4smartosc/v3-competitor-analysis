import json
from typing import Any
from agents import FunctionTool, RunContextWrapper
from pydantic import BaseModel
import requests
from config import SERPER_API_KEY

class DeepSearchOutput(BaseModel):
    web_page_text: str
        
class WebSearchToolItem(BaseModel):
    url: str
    "The URL required for deep web page search"
    
    class Config:  
        extra = "forbid" 
    
async def run_deep_search(data: WebSearchToolItem) -> DeepSearchOutput:
    url = "https://scrape.serper.dev"

    payload = json.dumps({
        "url": data.url
    })
    headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    json_data = response.json()
    web_page_text = json_data.get("text", "")
    return DeepSearchOutput(
        web_page_text=web_page_text,
    )
    
async def function_tool_run_deep_search(
    ctx: RunContextWrapper[Any], args: str
) -> str:
    """Function tool used for deep web search using Serper API."""
    print("Tool invoked with args:", args)
    web_search_payload = WebSearchToolItem.model_validate_json(args)
    return await run_deep_search(web_search_payload)

deep_dive_tool = FunctionTool(
    name="deep_dive_tool",
    description="Deep dive tool for web page search using Serper API.",
    params_json_schema=WebSearchToolItem.model_json_schema(),
    on_invoke_tool=function_tool_run_deep_search,
)
