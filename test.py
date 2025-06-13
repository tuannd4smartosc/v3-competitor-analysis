import json
from agents import Runner
from llm_agents.planner.agent import WebSearchPlan, planner_agent
from llm_agents.search.narrow_search.agent import SearchMetadata, SearchResult, SearchResultWithMetadata, search_agent, SearchResultsItem
from llm_agents.countries_detector.agent import countries_detector_agent, CountriesList
from llm_agents.search.tools.deep_dive_tool import WebSearchToolItem, run_deep_search # This tool is not directly used in the provided snippet's loop, but kept for completeness
from llm_agents.campaign.agent import Campaign, CampaignsList, campaign_agent
from llm_agents.csv_maker.agent import csv_maker_agent, CSVResult
from llm_agents.search.price_search.agent import price_research_agent
import asyncio
from utils import generate_csv_file_from_text

async def safe_run(agent, input, output_type, max_turns=3):
    """
    Safely runs an agent with error handling and a default max_turns.
    """
    try:
        # Pass max_turns to the Runner.run method
        result = await Runner().run(agent, input=input, max_turns=max_turns)
        return result.final_output_as(output_type)
    except Exception as e:
        print(f"Error running agent {agent.name} with input '{input[:50]}...': {e}")
        print("Skipping...")
        return None
    
async def detect_countries(region, company_name, company_competitors) -> CountriesList:
    countries_detector_prompt = f"List the ISO 3166-1 alpha-2 country codes for {region} where {company_name}, {company_competitors} operate in."
    countries_detector_output = await safe_run(
        countries_detector_agent,
        input=countries_detector_prompt,
        output_type=CountriesList
    )
    return countries_detector_output

async def generate_search_plan(company_name, company_competitors, country: str, date_range, topic: str) -> WebSearchPlan:
    planner_prompt = (
        f"Plan a web search that focus on {topic} from {company_name}, {company_competitors} in {country} in {date_range}."
    )
    # It's good practice to give planning agents more turns if needed
    plan = await safe_run(
        planner_agent,
        input=planner_prompt,
        output_type=WebSearchPlan,
        max_turns=5 # Increased max_turns for planner_agent
    )
    if plan:
        print(f"Search Plan for {country}: {plan.searches}")
    else:
        print(f"Failed to get search plan for {country}")
    return plan

async def run_promotion_campaigns(company_name, company_competitors, region, date_range):
    countries_list = await detect_countries(region, company_name, company_competitors)
    search_plan_tasks = [
        generate_search_plan(company_name, company_competitors, country.country_name, date_range, "promotion campaigns, advertisements or promotional discounts")
        for country in countries_list.countries
    ]
    search_plans = await asyncio.gather(*search_plan_tasks)
    all_searches = [search for plan in search_plans if plan for search in plan.searches]
    
    async def process_search(search_item) -> list[SearchResultWithMetadata]:
        search_prompt = (
            f"Search for: {search_item.query} in {search_item.country_code} "
            f"with type {search_item.search_type.value} and date range {search_item.date_range}"
        )
        search_result = await safe_run(
            search_agent,
            input=search_prompt,
            output_type=SearchResult
        )
        if not search_result:
            print(f"No search results for query: {search_item.query[:30]}...")
            return []

        threshold = 7
        filtered_results = [
            item for item in search_result.search_results if item.relativity_score >= threshold and item.is_official
        ]
        print(f"  Query '{search_item.query[:30]}...': Found {len(filtered_results)} relevant results (out of {len(search_result.search_results)})")
        return [SearchResultWithMetadata(
                    search_result_item=item,
                    metadata=SearchMetadata(
                        query=search_item.query,
                        country_code=search_item.country_code,
                        search_type=search_item.search_type.value
                    )
                )
                for item in filtered_results 
            ]

    # Create a list of tasks for all narrow searches
    narrow_search_tasks = [process_search(search_item) for search_item in all_searches]
    # Run them all concurrently
    search_results_lists = await asyncio.gather(*narrow_search_tasks)

    # Flatten the list of lists into a single list of SearchResultsItem
    search_results_items = [item for sublist in search_results_lists for item in sublist]
    print(f"\nTotal filtered search results items: {len(search_results_items)}")

    # --- Step 4: Deep Dive for Campaigns in Parallel ---
    print("\nPerforming deep dives for campaigns in parallel...")
    urls = []
    campaigns: list[Campaign] = []
    context_lines = [] # Collect context lines to write later
    
    context_lines.append(json.dumps([item.model_dump_json() for item in search_results_items]))
    
    deep_dive_tasks = [run_deep_search(WebSearchToolItem(url=item.search_result_item.url)) for item in search_results_items]
    deep_dive_results = await asyncio.gather(*deep_dive_tasks)
    print("deep_dive_results",deep_dive_results)
    
    print(f"Deep dive results: {len(deep_dive_results)} items")
        
    print(f"\nTotal campaigns found: {len(campaigns)}")
    # print("Campaigns found:", campaigns) # Uncomment if you want to see full campaign objects
    print(">>>> URLs processed:", len(urls), "unique URLs:", len(set(urls)))

    # --- Step 5: Write Outputs (Sequential) ---
    print("\nWriting outputs...")
    with open("context.txt", "w", encoding="utf-8") as file:
        file.write("".join(context_lines))
        
    print("\nWriting outputs...")
    with open("data.txt", "w", encoding="utf-8") as file:
        file.write("".join(json.dumps([item.model_dump_json() for item in deep_dive_results])))

    # with open("data.txt", "w", encoding="utf-8") as file:
    #     campaign_json = [campaign.model_dump_json() for campaign in campaigns]
    #     file.write(json.dumps(campaign_json, indent=2, ensure_ascii=False))

    print("Processing complete!")
    
    return "".join(context_lines)

async def main():
    company_name = input("Enter your company's name: ")
    company_competitors = input("Enter your competitors' names: ")
    region = input("Enter the region that you want to focus on: ")
    date_range = input("Enter the date range for the research: ")

    await run_promotion_campaigns(company_name, company_competitors, region, date_range)
    # await run_price_analysis(company_name, company_competitors, region, date_range)

if __name__ == "__main__":
    asyncio.run(main())