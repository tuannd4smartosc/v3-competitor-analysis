import json
from agents import Runner
from llm_agents.planner.agent import WebSearchPlan, planner_agent
from llm_agents.search.narrow_search.agent import SearchResult, search_agent, SearchResultsItem
from llm_agents.countries_detector.agent import countries_detector_agent, CountriesList
from llm_agents.search.tools.deep_dive_tool import run_deep_search # This tool is not directly used in the provided snippet's loop, but kept for completeness
from llm_agents.campaign.agent import Campaign, CampaignsList, campaign_agent
from llm_agents.csv_maker.agent import csv_maker_agent, CSVResult
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

async def main():
    # --- Step 1: Detect Countries (Sequential, as it's a prerequisite) ---
    countries_detector_prompt = "List the ISO 3166-1 alpha-2 country codes for Southeast Asia where Nike and Adidas operates in."
    print("Starting country detection...")
    countries_detector_output = await safe_run(
        countries_detector_agent,
        input=countries_detector_prompt,
        output_type=CountriesList
    )
    if not countries_detector_output:
        print("Failed to get countries detector output. Exiting.")
        return
    print("Countries Detector Output:", [c.country_name for c in countries_detector_output.countries])

    # --- Step 2: Get Search Plans in Parallel for each country ---
    print("\nGenerating search plans in parallel...")
    async def get_search_plan(country):
        planner_prompt = (
            f"Plan a web search that focus on promotion campaigns, advertisements or promotional discounts from Nike and Adidas in {country.country_name} in April 2025."
        )
        # It's good practice to give planning agents more turns if needed
        plan = await safe_run(
            planner_agent,
            input=planner_prompt,
            output_type=WebSearchPlan,
            max_turns=5 # Increased max_turns for planner_agent
        )
        if plan:
            print(f"Search Plan for {country.country_name}: {plan.searches}")
        else:
            print(f"Failed to get search plan for {country.country_name}")
        return plan

    search_plan_tasks = [
        get_search_plan(country)
        for country in countries_detector_output.countries
    ]
    search_plans = await asyncio.gather(*search_plan_tasks)
    all_searches = [search for plan in search_plans if plan for search in plan.searches]
    print(f"Total search queries generated: {len(all_searches)}")

    # --- Step 3: Execute Narrow Searches in Parallel ---
    print("\nExecuting narrow searches in parallel...")
    async def process_search(search_item) -> list[SearchResultsItem]:
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

        threshold = 0.7
        filtered_results = [
            item for item in search_result.search_results if item.relativity_score >= threshold
        ]
        print(f"  Query '{search_item.query[:30]}...': Found {len(filtered_results)} relevant results (out of {len(search_result.search_results)})")
        return filtered_results

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
    
    csv_agent_output = await safe_run(
        csv_maker_agent,
        input=f"Given this data: {json.dumps([search_item.model_dump_json() for search_item in search_results_items])}. \n\nGenerate a CSV file with the following columns: Campaign Name, Company Name, Start Date, End Date, Mechanic, Offerings, Country, Summary, URL",
        output_type=CSVResult
    )

    context_lines.append(json.dumps([search_item.model_dump_json() for search_item in search_results_items]))
    print("CSV Agent Output:", csv_agent_output)
    generate_csv_file_from_text(csv_agent_output.csv_file, "campaigns.csv")
    
    # async def deep_dive_and_extract_campaigns(result_item):
    #     if not result_item.need_deep_dive:
    #         print(f"Skipping deep dive for {result_item.url} as it does not need one.")
    #         return "", result_item.url, []
    #     context_line = f"Search Result: {result_item.search_result}\nURL: {result_item.url}\n"
    #     campaigns_result = await safe_run(
    #         campaign_agent,
    #         input=f"Deep dive into this url: {result_item.url} to find promotion campaigns from Asics in April 2025.",
    #         output_type=CampaignsList,
    #         max_turns=1 # Increased max_turns for deep_dive_agent
    #     )
    #     if campaigns_result:
    #         print(f"  Successfully extracted {len(campaigns_result.campaigns)} campaigns from {result_item.url}")
    #         return context_line, result_item.url, campaigns_result.campaigns
    #     else:
    #         print(f"  No campaigns or error for URL: {result_item.url}")
    #         return context_line, result_item.url, []

    # # Create tasks for all deep dives
    # deep_dive_tasks = [deep_dive_and_extract_campaigns(item) for item in search_results_items]
    # # Run them all concurrently
    # deep_dive_results = await asyncio.gather(*deep_dive_tasks)

    # Process the results from parallel deep dives
    # for ctx_line, url, extracted_campaigns in deep_dive_results:
    #     context_lines.append(ctx_line)
    #     urls.append(url)
    #     campaigns.extend(extracted_campaigns)

    print(f"\nTotal campaigns found: {len(campaigns)}")
    # print("Campaigns found:", campaigns) # Uncomment if you want to see full campaign objects
    print(">>>> URLs processed:", len(urls), "unique URLs:", len(set(urls)))

    # --- Step 5: Write Outputs (Sequential) ---
    print("\nWriting outputs...")
    with open("context.txt", "w", encoding="utf-8") as file:
        file.write("".join(context_lines))

    with open("data.txt", "w", encoding="utf-8") as file:
        campaign_json = [campaign.model_dump_json() for campaign in campaigns]
        file.write(json.dumps(campaign_json, indent=2, ensure_ascii=False))

    print("Processing complete!")

if __name__ == "__main__":
    asyncio.run(main())