
def generate_promotion_campaign_user_query(company_name, competitor_names, date_range, region):
    USER_QUERY = f"""
    List all **promotion campaigns**, **marketing activations**, and **noteworthy public campaigns or events** related to **{company_name}** and its competitors, **{competitor_names}**, that occurred within the date range **{date_range}**, specifically in **{region}**.

    Include all types of relevant activity:

    - **Product launches** (e.g., new SKUs, special editions, limited drops)
    - **Discount or voucher campaigns** (e.g., seasonal sales, app-only codes, bundle offers)
    - **Brand collaborations** (e.g., with celebrities, influencers, designers, or other brands)
    - **Region-specific marketing events** (e.g., in-store activations, pop-ups, mobile app campaigns)
    - **Digital/social campaigns** (e.g., hashtag drives, platform-specific promotions, gamified rewards)
    - **Public controversies or advocacy events** (e.g., backlash, labor protests, DEI statements, environmental campaigns)  
    - **Loyalty program campaigns** or promotions available only to members or app users

    **Do not include** campaigns outside of **{region}** or beyond the specified **{date_range}**.

    ---

    In addition to events strictly within the range, also include **adjacent or overlapping campaigns** that:

    - **Launched just before** {date_range} and remained active into it  
    - **Were announced or leaked within the timeframe**, even if execution is slightly later  
    - Are **seasonally aligned** (e.g., tied to "6.6", "mid-year", Ramadan, Back-to-School, etc.) and are likely coordinated across the region  
    - Show **cross-country consistency** or overlap in digital campaigns (e.g., similar app codes, same influencer partnerships)

    ---

    For each campaign or event, provide the following details:

    - **Campaign/Event Name or Hashtag**
    - **Exact Dates of the Campaign/Event**
    - **Products or Categories Involved** (e.g., footwear, apparel, accessories, limited collections)
    - **Quantitative Details** (e.g., % discount, price cut, voucher values, number of SKUs, audience reached)
    - **Channel(s) of Availability** (e.g., app-only, website, physical stores, TikTok, influencer page, livestream)
    - **Countries or Cities Affected** (be specific; avoid generalizations like “Southeast Asia”)
    - **Type of Campaign or Event** (e.g., Promotional, Advocacy, Controversy, Loyalty, Social Impact)

    ---

    Also include a section titled `Additional Strategic Insights` that analyzes:

    - Whether the campaign was part of a **regional trend or global alignment**  
    - Any **notable overlap between the brands** (e.g., both launching 6.6 sales, targeting the same demographic)  
    - Use of **loyalty programs or apps** to create exclusivity or extend discounts  
    - Any **country-specific anomalies or particularly aggressive pricing tactics**

    ---

    Finally, append a summary table with the following columns:

    | Brand | Campaign/Event Name | Date(s) | Key Products Affected | Quantitative Highlights | Channel(s) | Countries/Cities | Type |
    |-------|----------------------|--------|------------------------|-------------------------|-------------|------------------|------|

    If **no events or campaigns** were found for a brand during the specified period, **explicitly state this**. If applicable, also mention **when such campaigns usually occur** and if there were **notable missed opportunities** or **late-stage preparations** visible through press coverage, social media, or e-commerce channels.


    """
   

    return USER_QUERY
