
def generate_traffic_revenue_query(company_name, competitor_names, date_range, region):
    USER_QUERY = f"""
    "prompt_title": "Generate a Competitor Traffic & Revenue Performance Analysis Report with Visual Tables",
    "objective": (
        "Produce a comprehensive report analyzing traffic and revenue performance for the specified competitors, "
        "mirroring the structure and visual presentation of the SG performance dashboard using visual tables "
        "at both division and category levels."
    ),
    "input_parameters": {{
        "target_company": "{company_name}",
        "competitors": "{competitor_names}",
        "region": "{region}",
        "time_period": "{date_range}"
    }},
    "data_requirements": {{
        "dimensions": {{
            "division": ["Footwear", "Apparel", "Equipment"],
            "category": ["Running", "Basketball", "Young Athletes"]
        }},
        "metrics": [
            "Actual Revenue (USD)",
            "Revenue Growth (%) vs. previous year or baseline",
            "Pageviews",
            "Visitors",
            "Buyers",
            "Orders",
            "Units Sold",
            "AOV (Average Order Value in USD)",
            "AUR (Average Unit Retail in USD)",
            "ARPU (Average Revenue per User in USD)",
            "CR (B/V): Conversion Rate (Buyers / Visitors) in %",
            "CR (O/V): Conversion Rate (Orders / Visitors) in %",
            "% SOB: Share of Business (revenue-based)"
        ]
    }},
    "visual_output_instructions": {{
        "tables_per_competitor": [
            "Division-level summary table with traffic and revenue KPIs",
            "Category-level breakdown table",
            "YoY % change summary table with color-coded formatting",
            "Traffic vs. Revenue correlation table",
            "Revenue Share by Division and Category"
        ],
        "table_formatting_rules": [
            "Each table should display a maximum of 5 columns.",
            "If a table requires more than 5 metrics, split the content into multiple tables, each clearly labeled as part 1, part 2, etc.",
            "Ensure tables fit within the report layout without horizontal scrolling or overflow."
        ]
    }},
    "data_sources": [
        "Web analytics platforms (e.g., Similarweb, SEMrush)",
        "Retail & marketplace data (e.g., Shopee, Lazada, Amazon, brand.com)",
        "Industry reports (e.g., Statista, Euromonitor, NielsenIQ)",
        "Third-party data aggregators (e.g., DataWeave, Profitero)",
        "Publicly disclosed financials and press releases"
    ],
    "insights_summary": {{
        "instructions": "At the end of each competitor’s section, summarize 3–4 insights focused on traffic and revenue trends.",
        "insight_types": [
            "Total traffic and buyer volume trends",
            "High- or low-performing divisions/categories by revenue",
            "Shifts in conversion performance",
            "Notable changes in revenue share vs. prior period"
        ]
    }},
    "additional_instructions": [
        "Repeat the analysis structure for each competitor in {competitor_names}.",
        "Use real or estimated values and label estimates clearly.",
        "Maintain consistent numeric formatting (USD values, percentages to 2 decimal places)."
    ]
    """

    return USER_QUERY
