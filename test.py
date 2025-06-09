from agents import Runner
from llm_agents.planner.agent import WebSearchPlan, planner_agent
from llm_agents.search.narrow_search.agent import SearchResult, search_agent
from llm_agents.search.tools.deep_dive_tool import run_deep_search

async def main():
    planner_prompt = "Plan a web search that focus on promotion campaigns from Nike and Adidas in Southeast Asia in June 2025."
    search_plan_output = await Runner().run(
        planner_agent,
        input=planner_prompt
    )
    search_plan = search_plan_output.final_output_as(WebSearchPlan)
    print("Search Plan:", search_plan)
    context = ""
    for search_item in search_plan.searches:
        search_prompt = f"Search for: {search_item.query} in {search_item.country_code} with type {search_item.search_type.value} and date range {search_item.date_range}"
        search_output = await Runner().run(
            search_agent,
            input=search_prompt
        )
        search_result = search_output.final_output_as(SearchResult)
        
        threshold = 0.8
        
        filtered_results = [
            item for item in search_result.search_results if item.relativity_score >= threshold
        ]
        
        print(len(filtered_results), len(search_result.search_results))
        
        for item in filtered_results:
            if item.need_deep_dive:
                print(f"Deep Dive Needed for {item.search_result} from {item.url}")
                deep_dive_output = run_deep_search(item.url)
                print(f"Deep Dive Result for {item.url}:", deep_dive_output.web_page_text)
                context += deep_dive_output.web_page_text + "\n\n"
            context += item.search_result + "\n\n"

    print("Final Context:", context)
    
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())