import asyncio
from manager import ResearchManager
from printer import Printer


def generate_price_analysis_user_query(company_name, competitor_names, date_range, region):
    USER_QUERY = f"""
    Write a data-driven price comparison analysis report section for the sportswear industry, focusing on:
    - Target Company: {company_name}
    - Competitors: {competitor_names}
    - Region: {region}
    - Time Period: {date_range}

    Instructions:
    - Do NOT include an introduction, background context, or any explanatory narrative.
    - Minimize prose. Focus on structured tables and quantitative data.
    - Use consistent formatting in all tables.

    Report Components:

    1. Product Segment Analysis
    For each product segment (e.g., Footwear, Apparel, Accessories, Equipment):
    - Include at least 10 products per brand.
    - Group products by brand and rank them by popularity or relevance.
    - Present the following columns in a table:
    - Brand
    - Product Name
    - Brief Description
    - Original Price (USD)
    - Discounted Price (USD)
    - Country
    - Customer segment

    Repeat this table for each product segment.

    3. Overall Price Comparison Summary
    Include summary tables showing:
    - Average price per brand across all segments
    - Highest and lowest priced items per brand
    - Price spread (standard deviation) per brand
    - Country

    Use as many tables as possible. Avoid paragraphs or extended text. Keep the report concise and data-rich.

    """
    return USER_QUERY

def run_pricing_analysis(company_name, competitor_names, date_range, region, printer):
    manager_id = f"price_{company_name}_ca_{date_range}_{region}"
    user_prompt = generate_price_analysis_user_query(company_name, competitor_names, date_range, region)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    research_manager = ResearchManager(manager_id, printer)
    result = loop.run_until_complete(research_manager.run(user_prompt))
    return result