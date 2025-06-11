from enum import Enum
import json
from typing import Any
from pydantic import BaseModel
from agents import FunctionTool, RunContextWrapper
import requests
from config import SERPER_API_KEY

class NarrowSearchOutput(BaseModel):
    search_result: str
    url: str
        
class WebSearchToolType(Enum):
    web_search = "web_search"
    news_search = "news_search"

class WebSearchToolItem(BaseModel):
    query: str
    "The search term to use for the web search."
        
    country_code: str
    "ISO 3166-1 alpha-2 country code to filter the search results by country (e.g., 'th', 'sg', 'vn', 'id')."

    search_type: WebSearchToolType
    "Type of search required. The type must be either web_search or news_search."
    
    date_range: str
    "Date range for the search results in Google Search tbs format (e.g., 'cdr:1,cd_min:1/1/2024,cd_max:12/31/2025')."

    class Config:  
        extra = "forbid" 
    
def search_normal(query: str, country_code: str, date_range: str) -> list[NarrowSearchOutput]:
    url = "https://google.serper.dev/search"

    payload = json.dumps({
        "q": query,
        "gl": country_code,
        "tbs": date_range
    })
    
    headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    json_data = response.json()
    organic_results = json_data["organic"]
    results = [NarrowSearchOutput(
        search_result=f"Title: {item.get('title', '')}\nSnippet: {item.get('snippet', '')}",
        url=item.get("link", "")
    ) for item in organic_results]
    return results

def search_news(query: str, country_code: str, date_range: str) -> list[NarrowSearchOutput]:
    url = "https://google.serper.dev/news"

    payload = json.dumps({
        "q": query,
        "gl": country_code,
        "num": 10,
        "tbs": date_range
    })
    headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    json_data = response.json()
    news = json_data["news"]
    results = [NarrowSearchOutput(
        search_result=f"Title: {item.get('title', '')}\nSummary: {item.get('section', '')}",
        url=item.get("link", "")
    ) for item in news]
    return results

# def search_shopping(query: str, country_code: str, date_range: str) -> list[NarrowSearchOutput]:
#     url = "https://google.serper.dev/shopping"

#     payload = json.dumps({
#         "q": query,
#         "gl": country_code,
#         "num": 10,
#         "tbs": date_range
#     })
#     headers = {
#         'X-API-KEY': SERPER_API_KEY,
#         'Content-Type': 'application/json'
#     }

#     response = requests.request("POST", url, headers=headers, data=payload)
#     json_data = response.json()
#     shopping_results = json_data["shopping"]
#     print("shopping_results", shopping_results)
#     results = [NarrowSearchOutput(
#         search_result=f"Title: {item.get('title', '')}\nPrice: {item.get('price', '')}\nRating: {item.get('rating', '')}\nRating Count: {item.get('rating_count', '')}",
#         url=item.get("link", "")
#     ) for item in shopping_results]
#     return results

# def search_places(query: str, country_code: str, date_range: str) -> list[NarrowSearchOutput]:
#     url = "https://google.serper.dev/places"

#     payload = json.dumps({
#         "q": query,
#         "gl": country_code,
#         "num": 10,
#         "tbs": date_range
#     })
#     headers = {
#         'X-API-KEY': SERPER_API_KEY,
#         'Content-Type': 'application/json'
#     }
#     response = requests.request("POST", url, headers=headers, data=payload)
#     json_data = response.json()
#     places = json_data["places"]
#     print("places",places)
#     results = [NarrowSearchOutput(
#         search_result=f"Title: {item.get('title', '')}\nAddress: {item.get('address', '')}\nRating: {item.get('rating', '')}\nRating Count: {item.get('rating_count', '')}\nPhone: {item.get('phone', '')}\nLongitude: {item.get('longitude', '')}\nLatitude: {item.get('latitude', '')}",
#         url=item.get("link", "")
#     ) for item in places]
#     return results
    

async def run_search(data: WebSearchToolItem) -> list[NarrowSearchOutput]:
    query = data.query
    country_code = data.country_code
    search_type = data.search_type
    date_range = data.date_range
    
    if search_type.value == WebSearchToolType.web_search.value:
        return search_normal(query, country_code, date_range)
    elif search_type.value == WebSearchToolType.news_search.value:
        return search_news(query, country_code, date_range)
    return []
    
async def function_tool_run_search(
    ctx: RunContextWrapper[Any], args: str
) -> str:
    """Function tool used for the web search using Serper API."""
    web_search_payload = WebSearchToolItem.model_validate_json(args)
    return await run_search(web_search_payload)

narrow_search_tool = FunctionTool(
    name="serper_web_search_tool",
    description="Serper Web Search Tool for performing different types of web searches based on user queries.",
    params_json_schema=WebSearchToolItem.model_json_schema(),
    on_invoke_tool=function_tool_run_search,
)