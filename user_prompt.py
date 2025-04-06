
# Generate prompt function from your original script
def generate_prompt(company_name: str, competitor_names: str, date: str, region: str) -> str:
    return (
        f"""
        Generate a comprehensive competitor analysis report for **{company_name}** versus **{competitor_names}** in **{region}** 
        for the date range: **{date}**. 

        The report must focus on the **promotional campaigns** of both {company_name} and its competitors. For each campaign, include:

        1. **Regions Launched** – List all regions where the campaign was launched.
        2. **Campaign URL** – Include a direct link to the campaign if available.
        3. **Campaign Overview** – Describe the campaign’s goals, creative strategy, messaging, and marketing channels used.
        4. **Products Promoted or Launched** – List all featured products.
        5. **Pricing Information** – Provide a table of product prices across regions, if available.
        6. **Key Performance Indicators (KPIs)** – Include relevant KPIs such as impressions, CTR, conversions, ROI, etc., with supporting statistics and evidence.
        7. **Target Audience** – Break down customer segments by demographics, behavior, and preferences. Include **percentages and statistics** for each segment in {region}.
        8. **Revenue Impact** – Provide data and percentages showing how the campaign influenced the company’s revenue.
        9. **Market Impact** – Analyze how each campaign affected the {region} market in terms of **revenue, market share, and customer engagement**, supported by data.
        10. **Key Events & Timing** – Highlight major events or seasonal factors during the date range and assess how they influenced campaign performance.
        11. **Competitive Impact** – Analyze how each competitor’s campaign impacted {company_name}'s positioning, with market response and data.
        12. **Reference Links** – Include credible links for all data sources, claims, or statistics.

        Finally, based on your analysis, suggest **a strategic action plan** for {company_name} to improve its market position and campaign effectiveness in {region}.
        """
    )