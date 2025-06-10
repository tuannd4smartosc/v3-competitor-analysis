import json
from agents import Runner
from llm_agents.planner.agent import WebSearchPlan, planner_agent
from llm_agents.search.narrow_search.agent import SearchResult, search_agent, SearchResultsItem
from llm_agents.countries_detector.agent import countries_detector_agent, CountriesList
from llm_agents.search.tools.deep_dive_tool import run_deep_search
from llm_agents.campaign.agent import Campaign, CampaignsList, campaign_agent

async def safe_run(agent, input, output_type):
    try:
        result = await Runner().run(agent, input=input, max_turns=3)
        return result.final_output_as(output_type)
    except Exception as e:
        print(f"Error running agent {agent}: {e}")
        print("Skipping...")
        return None

async def main():
    countries_detector_prompt = "List the ISO 3166-1 alpha-2 country codes for Southeast Asia where Nike operates in."
    countries_detector_output = await safe_run(
        countries_detector_agent,
        input=countries_detector_prompt,
        output_type=CountriesList
    )
    if not countries_detector_output:
        print("Failed to get countries detector output.")
        return
    print("Countries Detector Output:", countries_detector_output)
    
    async def get_search_plan(country):
        planner_prompt = (
            f"Plan a web search that focus on promotion campaigns, advertisements or promotional discounts from Asics in {country.country_name} in April 2025."
        )
        search_plan = await safe_run(
            planner_agent,
            input=planner_prompt,
            output_type=WebSearchPlan
        )
        print("Search Plan:", search_plan)
        return search_plan

    tasks = [
        get_search_plan(country)
        for country in countries_detector_output.countries
    ]
    import asyncio
    search_plans = await asyncio.gather(*tasks)
    all_searches = [search for plan in search_plans if plan for search in plan.searches]
    
    urls = []
    campaigns: list[Campaign] = []
    context = ""
    
    async def process_search(search_item) -> list[SearchResultsItem]:
        search_prompt = f"Search for: {search_item.query} in {search_item.country_code} with type {search_item.search_type.value} and date range {search_item.date_range}"
        search_result = await safe_run(
            search_agent,
            input=search_prompt,
            output_type=SearchResult
        )
        if not search_result:
            return []
        threshold = 0.7
        filtered_results = [
            item for item in search_result.search_results if item.relativity_score >= threshold
        ]
        print("filtered_results:", len(filtered_results), "search_result:", len(search_result.search_results))
        print("filtered_results", filtered_results)
        return filtered_results

    search_results_lists: list[list[SearchResultsItem]] = []
    for search_item in all_searches:
        results = await process_search(search_item)
        search_results_lists.append(results)
    search_results_items = [item for sublist in search_results_lists for item in sublist]
    print("search_results_items", search_results_items)
    print("Total search results:", sum(len(results) for results in search_results_lists))
    for result in search_results_items:
        context += f"Search Result: {result.search_result}\nURL: {result.url}\n"
        campaigns_result = await safe_run(
            campaign_agent,
            input=f"Deep dive into this url: {result.url} to find promotion campaigns from Asics in April 2025.",
            output_type=CampaignsList
        )
        print("Campaigns Result:", campaigns_result)
        if campaigns_result:
            campaigns.extend(campaigns_result.campaigns)
        urls.append(result.url)

    print("Campaigns found:", len(campaigns), campaigns)
    print(">>>>> urls:", urls)
    
    with open("context.txt", "w", encoding="utf-8") as file:
        file.write(context)

    with open("data.txt", "w", encoding="utf-8") as file:
        campaign_json = [campaign.model_dump_json() for campaign in campaigns]
        file.write(json.dumps(campaign_json, indent=2, ensure_ascii=False))
    
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())