
def generate_traffic_revenue_query(company_name, competitor_names, date_range, region):
    USER_QUERY = f"""
    {{
    "prompt_title": "Generate a Country-Specific within {region} and {date_range} Competitor Traffic & Revenue Performance Analysis Report with Visual Tables",
    "objective": (
        "Produce a comprehensive report analyzing traffic and revenue performance for the specified competitors "
        "within each country (or major city, if applicable) in the selected region. Structure and visualize data similar "
        "to the SG performance dashboard, but focus on intra-country performance across divisions and categories. "
        "Include year-over-year or period-over-period percentage changes for all key metrics with color-coded formatting."
    ),
    "input_parameters": {{
        "target_company": "{company_name}",
        "competitors": "{competitor_names}",
        "region": "{region}",
        "time_period": "{date_range}"
    }},
    "data_requirements": {{
        "dimensions": {{
        "division": [
            "Footwear",
            "Apparel",
            "Accessories",
            "Equipment",
            "Digital Products & Subscriptions",
            "Wellness & Lifestyle Gear"
        ],
        "category": [
            "Running",
            "Basketball",
            "Football/Soccer",
            "Training & Gym",
            "Outdoor & Trail",
            "Casual/Lifestyle",
            "Youth & Young Athletes",
            "Women's Performance",
            "Men's Essentials",
            "Unisex Core",
            "Sustainable/Green Product Lines",
            "Tech-Integrated Products"
        ]
        }},
        "metrics": [
        "Actual Revenue (in local currency)",
        "Revenue Growth (%) vs. previous year or baseline",
        "Pageviews",
        "Visitors",
        "Buyers",
        "Orders",
        "Units Sold",
        "AOV (Average Order Value in local currency)",
        "AUR (Average Unit Retail in local currency)",
        "ARPU (Average Revenue per User in local currency)",
        "CR (B/V): Conversion Rate (Buyers / Visitors) in %",
        "CR (O/V): Conversion Rate (Orders / Visitors) in %",
        "% SOB: Share of Business (revenue-based)"
        ]
    }},
    "visual_output_instructions": {{
        "tables_per_competitor": [
        "Division-level summary table by country (or city) with traffic and revenue KPIs",
        "Category-level breakdown table per country",
        "YoY % change summary table with color-coded formatting per country",
        "Traffic vs. Revenue correlation table for each geography",
        "Revenue Share by Division and Category within each country",
        "Top 10 or Top 20 Products Table by Country"
        ],
        "table_formatting_rules": [
        "Each table should display a maximum of 5 columns.",
        "If a table requires more than 5 metrics, split the content into multiple tables, each clearly labeled as part 1, part 2, etc.",
        "Ensure tables fit within the report layout without horizontal scrolling or overflow.",
        "In YoY % change columns, use color-coded formatting: green for positive %, red for negative %, gray for 0% change."
        ]
    }},
    "top_products_table": {{
        "description": "Rank the top 10 or 20 products across all brands *within each country or city* in the specified region and date range, based on total units sold or revenue. All rankings must be derived from reliable third-party sources.",
        "columns": [
        "Rank",
        "Brand",
        "Product Name",
        "Category",
        "Revenue (local currency)",
        "Units Sold",
        "Price Change %",
        "Country/City",
        "Ranking Source"
        ],
        "formatting": "Use color coding for Price Change %: green for negative (discount), red for positive (price increase), gray for no change. Rank must be sorted by Revenue or Units Sold. Include a reference or footnote for the ranking source (e.g., Euromonitor, NielsenIQ, Shopee Top Products, Lazada Trending, etc.). If no credible ranking source is found, exclude the product from the table."
    }},
    "data_sources": [
        "Web analytics platforms (e.g., Similarweb, SEMrush)",
        "Retail & marketplace data (e.g., Shopee, Lazada, Amazon, brand.com)",
        "Industry reports (e.g., Statista, Euromonitor, NielsenIQ)",
        "Third-party data aggregators (e.g., DataWeave, Profitero)",
        "Publicly disclosed financials and press releases"
    ],
    "insights_summary": {{
        "instructions": "At the end of each competitor’s section for each country, summarize 3–4 insights focused on traffic and revenue trends.",
        "insight_types": [
        "Total traffic and buyer volume trends by country",
        "High- or low-performing divisions/categories by revenue in each geography",
        "Shifts in conversion performance within the country",
        "Notable changes in revenue share vs. prior period at the local level"
        ]
    }},
    "additional_instructions": [
        "Repeat the full analysis structure for each country (or city) within {region} and for each competitor in {competitor_names}.",
        "Use real or estimated values and label estimates clearly.",
        "Include percentage change calculations where applicable and apply color formatting to highlight key movements.",
        "Maintain consistent numeric formatting (local currency values, percentages to 2 decimal places)."
    ]
    }}
    """



    return USER_QUERY
