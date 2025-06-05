import asyncio
from manager import ResearchManager
from printer import Printer


def generate_traffic_revenue_query(company_name, competitor_names, date_range, region):
    USER_QUERY = f"""
    # Prompt: Generate a Competitor Pricing Analysis Report

    ## Objective
    Produce a comprehensive pricing analysis report for the specified competitors, replicating the structure and visual presentation of the SG performance dashboard.

    ## Input Parameters
    - Target Company: {company_name}
    - Competitors: {competitor_names} (analyze each competitor individually)
    - Region: {region}
    - Time Period: {date_range}

    ## Data Requirements
    For each competitor, extract or estimate the following performance metrics at both the division and category levels:

    - Dimensions:
    - Division: Footwear, Apparel, Equipment
    - Category: e.g., Running, Basketball, Young Athletes

    - Metrics:
    - Actual Demand
    - Demand Change (%) relative to previous year or baseline
    - Units Sold
    - Orders
    - Buyers
    - Pageviews
    - Visitors
    - AOV (Average Order Value in USD)
    - AUR (Average Unit Retail in USD)
    - ARPU (Average Revenue per User in USD)
    - CR (B/V): Conversion Rate (Buyers / Visitors) in %
    - CR (O/V): Conversion Rate (Orders / Visitors) in %
    - % SOB: Share of Business in percentage points

    ## Visual Formatting Instructions
    - Follow the SG dashboard layout structure and hierarchy.
    - Apply conditional formatting:
    - Use green for positive % changes and red for negative ones.
    - Adjust color intensity to reflect magnitude (e.g., bright green for ≥ +30%, dark red for ≤ -50%).
    - Ensure clean formatting with logical groupings and consistent order of metrics.

    ## Data Sources
    Use a combination of publicly available and third-party intelligence sources, including:
    - Retail and marketplace sites (e.g., Amazon, Shopee, Lazada, brand.com)
    - Web analytics platforms (e.g., Similarweb, SEMrush)
    - Pricing and inventory tracking tools (e.g., Profitero, DataWeave)
    - Industry research (e.g., Statista, Euromonitor, NielsenIQ)
    - Public company data and press releases

    ## Insights Summary
    At the end of each competitor's section, include a concise bullet-point summary with 3–4 insights covering:
    - Overall performance trends
    - High- or low-performing divisions or categories
    - Notable shifts in traffic, conversions, or pricing
    - Market share movement or competitive repositioning

    ## Additional Instructions
    - Repeat the structure above for each competitor in {competitor_names}.
    - Use real numerical values wherever possible.
    - Clearly indicate any estimated values and document the source or rationale for estimates.
    - Format all numerical values consistently (e.g., percentages to two decimal places, currency in USD).

    """
    return USER_QUERY

def run_traffic_revenue_analysis(company_name, competitor_names, date_range, region, printer):
    manager_id = f"revenue_{company_name}_{date_range}_{region}"
    user_prompt = generate_traffic_revenue_query(company_name, competitor_names, date_range, region)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    research_manager = ResearchManager(manager_id, printer)
    result = loop.run_until_complete(research_manager.run(user_prompt))
    return result