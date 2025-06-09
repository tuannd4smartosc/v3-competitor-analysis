from enum import Enum
import json
from pydantic import BaseModel
import requests
from config import SERPER_API_KEY

class DeepSearchOutput(BaseModel):
    web_page_text: str
    url: str
        
class WebSearchToolItem(BaseModel):
    url: str
    "The URL required for deep web page search"
    
    class Config:  
        extra = "forbid" 
    
def run_deep_search(link: str) -> DeepSearchOutput:
    url = "https://scrape.serper.dev"

    payload = json.dumps({
        "url": link
    })
    headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    json_data = response.json()
    return DeepSearchOutput(
        web_page_text=json_data["text"],
        url=link
    )

    