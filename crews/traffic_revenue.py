import asyncio
from manager import ResearchManager
from printer import Printer


def generate_traffic_revenue_query(company_name, competitor_names, date_range, region):
    USER_QUERY = f"""
    Generate three separate multi-line line charts to compare performance metrics between {company_name} and its competitors ({competitor_names}), using a time-series x-axis and extending each chart 3 periods beyond the specified date range.

    **Region of Analysis:** {region}  
    **Time Period:** {date_range} (e.g., 2022–2024)  
    **Forecast Extension:** 3 future periods beyond the end of {date_range}, following the same time granularity (e.g., monthly or yearly).

    ---

    ### 1. Revenue Chart (CompanyRevenue Time Series)
    - **Data Source:** Use structured revenue data from the `CompetitorsRevenueData` model, where each record includes:
    - `company_name`: Name of the company
    - `revenue`: Total revenue
    - `year`: The corresponding year of the record
    - **Chart Type:** Multi-line line chart
    - **X-Axis:** Time (from the start of {date_range} to 3 years beyond)
    - **Y-Axis:** Revenue ($)
    - **Lines:** One per company (`company_name`), with values from `revenue` field
    - **Forecasts:** Forecast revenue for 3 additional years for each company using linear trends or available projections
    - **Style:** Forecasted lines must appear visually distinct (e.g., dashed lines or lighter color tones)

    ---

    ### 2. Clickstream Chart
    - **Metrics:** Total Visits, Unique Visitors, Bounce Rate (assumed available in similar structure to `CompanyRevenue`)
    - **X-Axis:** Same time series used in Revenue Chart
    - **One chart for each metric**, each using a multi-line line chart (one line per company)
    - **Include:** Historical values, current year, and 3 future forecast periods
    - **Visual Separation:** Forecasted segments should be dashed or styled differently

    ---

    ### 3. Traffic Sources Chart
    - **Metrics:** Direct Traffic, Referral Traffic, Organic Search Traffic
    - **Structure:** Same as above
    - **Include:** Full time series and forecasted periods
    - **Company Lines:** Each metric has a separate chart with one line per company

    ---

    ### Chart Formatting Requirements
    - Multi-line line charts with shared x-axis for time
    - X-axis granularity must match time intervals in `year` field (typically yearly)
    - All lines must be clearly labeled in the legend
    - Include chart title, x/y-axis labels, and distinguish forecasted data
    - Maintain consistent scaling across comparable charts

    ---

    ### Summary Table (Performance Overview)
    - Format similar to Nike's sales table
    - **Rows:** Countries (or markets) with optional sub-rows for categories (if available)
    - **Columns:**
    - Demand, Demand vs LY (%), Units, Orders, Buyers, Pageviews, Visitors
    - AOV, AUR, ARPU, CR (B/V), CR (O/V), % Share of Business (pts)
    - **Visual Cues:** Color-code positive growth (green) vs. negative growth (red)
    - **Aggregation:** Include total and average rows per region and company
    - **Footnotes:** Add concise footnotes summarizing trends, growth drivers, or anomalies

    ---

    ### Output Guidelines
    - All charts and tables must be suitable for presentation in strategic business reports
    - Label all elements clearly
    - Avoid placeholder data—use real values provided in the input


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