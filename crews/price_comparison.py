def generate_price_analysis_user_query(company_name, competitor_names, date_range, region):
    USER_QUERY = f"""
Write a data-driven **price comparison analysis report** for the sportswear industry, structured by **individual country or major city** within the specified region.

Focus on:
- Target Company: {company_name}
- Competitors: {competitor_names}
- Region: {region} (analyzed per country or major city)
- Time Period: {date_range}

Data Sources:
- Online marketplaces: Lazada, Footlocker, JD Sports, Zalora
- Official brand websites
- Social media platforms (e.g., Instagram, Facebook, Twitter, TikTok) for promotional pricing and trends

Instructions:
- Do NOT include introductions, background context, or narrative explanations.
- Minimize prose. Focus exclusively on **structured tables and quantitative comparisons**.
- Maintain consistent formatting and apply the same layout for every country or city in the region.
- Include both price increases and discounts. Highlight notable increases for high-demand products.
- Calculate and display **Price Change %** as:
    (Discounted Price – Original Price) / Original Price × 100
- Apply color formatting:
    - **Green** for negative % (price decrease/discount)
    - **Red** for positive % (price increase)
    - **Gray** for 0% change (no adjustment)

Report Structure (repeat all sections below for **each country or major city** in {region}):

---

1. **Product Segment Analysis** (by country or city)  
For each product segment (e.g., Footwear, Apparel, Accessories, Equipment, Digital Gear, Wellness):
- Include at least 5 products per brand per country/city.
- Use reliable price sources: Lazada, Footlocker, JD Sports, Zalora, brand websites, verified social media promotions.
- Rank products by popularity or relevance per local market.
- Table columns:
    - Country/City
    - Brand
    - Product Name
    - Brief Description
    - Original Price (local currency)
    - Adjusted Price (local currency)
    - Price Change %
    - Customer Segment

Repeat this table for each product segment and **every location in {region}**.

---

2. **Local Price Comparison Summaries**  
Include **all three tables below for every country or city** in {region}:

**a. Average Price per Brand (All Segments)**  
Columns:
- Country/City
- Brand
- Average Original Price (local currency)
- Average Adjusted Price (local currency)
- Average Price Change % (color-coded)

**b. Highest and Lowest Priced Items per Brand**  
Columns:
- Country/City
- Brand
- Highest Priced Item (local currency)
- Lowest Priced Item (local currency)

**c. Price Spread (Standard Deviation) per Brand**  
Columns:
- Country/City
- Brand
- Price Standard Deviation (local currency)

---

Visual Formatting Rules:
- Use clear, compact tables for all data.
- Color-code all **Price Change %** cells: green for discounts, red for markups, gray for no change.
- Format all numeric values consistently (two decimal places for currency and percentages).
- If a value is unavailable, indicate with “N/A” and note the data gap if needed.

---

Ensure the **entire report is organized as repeating blocks**, one for **each country or major city** in {region}, with consistent structure and styling.
"""


    return USER_QUERY
