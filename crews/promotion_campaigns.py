
def generate_promotion_campaign_user_query(company_name, competitor_names, date_range, region):
    USER_QUERY = f"""
    **Prompt: Competitor Analysis Report Generation**

    Please generate a **comprehensive competitor analysis report section** for **{company_name}** and its key competitors: **{competitor_names}**, focused on the **{region}** market during the period **{date_range}**.

    The section must follow a **professional structure** and contain detailed, data-driven content. Organize all insights by company and country. Use clear markdown formatting with headings, bullet points, and comparison tables. Prioritize readability and strategic depth.

    ---

    ### **1. Executive Summary**

    Provide a concise overview that includes:

    - The most important findings from the competitive analysis.
    - Key takeaways and **strategic implications** for **{company_name}**, based on how it compares to its competitors.

    ---

    ### **2. Deep Dive: Promotional Campaigns Analysis**

    For each company, present a detailed breakdown of **promotional campaigns**, organized **by country** within the region.

    Include the following campaign attributes:

    - **Campaign Name** and brief **Description**
    - **Geographic Coverage**: Countries targeted within {region}
    - **Campaign Timeline**: Start date and duration
    - **Marketing Channels Used**: e.g., Instagram, TikTok, YouTube, WeChat, TV, retail, email, e-commerce
    - **Products Promoted**: Specific SKUs or product families (e.g., "Air Max 270")
    - **Pricing Strategy**: Base price, discounts, bundling, flash sales, etc.
    - **Campaign Objectives**: e.g., brand awareness, conversions, loyalty, clearance
    - **Target Audience**: Demographic and psychographic profile
    - **Campaign Mechanics**: e.g., influencer partnerships, user-generated content, contests, retargeting
    - **Performance Metrics**:  
    - Impressions  
    - Click-Through Rate (CTR)  
    - Conversion Rate  
    - Return on Investment (ROI)  
    - Engagement Rate

    #### **Comparison Tables (required):**

    Use **multiple side-by-side tables** to compare campaign elements. Keep each table to **no more than 5 columns** for clarity.

    Suggested tables:

    - 📦 **Product Focus Table**: Popular SKUs and campaign insights by brand  
    - 🎯 **Target Audience vs. Campaign Objective**  
    - 📱 **Channel Breakdown**: Separate table per platform (e.g., Instagram, WeChat, TikTok, etc.)  
    - 📊 **Performance Metrics Comparison**  
    - 🧩 Add any other relevant tables — the more detailed and organized, the better

    ---

    ### **3. Data Visualization Requirements**

    Add clear data visualization placeholders:

    - **Campaign Comparison Table**: By country and company
    - **Channel Effectiveness Table**: Reach and CTR per marketing channel
    - **Pricing Strategy Table**: Original vs. discount/bundle pricing
    - **Performance Metrics Table**: Side-by-side KPI summary

    ---

    ### **Formatting Guidelines**

    - Use **markdown headings**, **bullet points**, and **tables** to improve readability
    - Limit tables to **5 columns max** each
    - Include **Harvard-style citations** for all third-party sources, case studies, or performance data
    - Avoid using placeholder text for data unless absolutely necessary; real values from the context are preferred
    - Do not include a conclusion
    """
    return USER_QUERY
