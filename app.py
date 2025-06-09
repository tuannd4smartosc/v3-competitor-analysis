import streamlit as st
import os
from datetime import datetime
import asyncio
from dotenv import load_dotenv
from manager import AiManager
from config import REPORT_DIR
from utils import show_confetti, get_pdf_download_link, sort_file_names
from st_printer import Printer
import datetime

load_dotenv()

st.set_page_config(page_title="MIRA: Marketing Intelligence & Research Agent", layout="wide", initial_sidebar_state="expanded")

st.sidebar.title("Reports")

if not os.path.exists(REPORT_DIR):
    os.makedirs(REPORT_DIR)

all_report_files = [f for f in os.listdir(REPORT_DIR) if f.endswith(".md")]

focus_regions = set()
for file in all_report_files:
    parts = file.split('_')
    if len(parts) >= 4:
        region = parts[3].split('-')[0] if '-' in parts[3] else parts[3]
        focus_regions.add(region)

focus_regions = ["All"] + sorted(list(focus_regions))
selected_region = st.sidebar.selectbox("Filter by Focus Region", focus_regions)

file_dates = []
for file in all_report_files:
    try:
        parts = file.split('_')
        if len(parts) >= 4 and '-' in parts[3]:
            region_date_part = parts[3]
            date_str = region_date_part.split('-')[1]
            if len(date_str) >= 8 and date_str.isdigit():
                year = int(date_str[:4])
                month = int(date_str[4:6])
                day = int(date_str[6:8])
                file_date = datetime.date(year, month, day)
                file_dates.append(file_date)
    except (ValueError, IndexError):
        continue

if file_dates:
    min_date = min(file_dates)
    max_date = max(file_dates)
else:
    current_date = datetime.date.today()
    min_date = current_date
    max_date = current_date

st.sidebar.subheader("Filter by Date Created")
date_filter = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

filtered_reports = []
for file in all_report_files:
    region = ""
    file_date = None
    
    try:
        parts = file.split('_')
        if len(parts) >= 4 and '-' in parts[3]:
            region_date_part = parts[3]
            region_parts = region_date_part.split('-')
            region = region_parts[0]
            
            if len(region_parts) > 1:
                date_str = region_parts[1]
                if len(date_str) >= 8 and date_str.isdigit():
                    year = int(date_str[:4])
                    month = int(date_str[4:6])
                    day = int(date_str[6:8])
                    file_date = datetime.date(year, month, day)
    except (ValueError, IndexError):
        continue
    
    date_match = True
    if file_date and len(date_filter) == 2:
        date_match = date_filter[0] <= file_date <= date_filter[1]
    elif file_date is None:
        date_match = True
    
    region_match = selected_region == "All" or region == selected_region
    
    if date_match and region_match:
        filtered_reports.append(file)

md_reports = sort_file_names(filtered_reports)

# 🟢 Check if a new report was just generated
if "new_report" in st.session_state and st.session_state["new_report"] in md_reports:
    default_report_index = md_reports.index(st.session_state["new_report"])
    selected_report = st.sidebar.selectbox("Select a Report", md_reports, index=default_report_index)
    del st.session_state["new_report"]
else:
    selected_report = st.sidebar.selectbox("Select a Report", md_reports if md_reports else ["No reports match your filters"])

st.title("MIRA: Marketing Intelligence & Research Agent")
st.markdown("Analyze Nike's competitor pricing and promotions with a single click!")

company_name = "Nike"

default_competitors = [
    "Adidas", "Levis", "New Balance", "Lululemon", "Puma",
    "Sketchers", "Under Armour", "Reebok", "ASICS", "Fila"
]

competitor_names = st.multiselect("Competitors' Names", 
                                  default_competitors,
                                  accept_new_options=True,
                                  )

today = datetime.date.today()
start_date = today
end_date = today.replace(year=today.year + 5)

default_start = today - datetime.timedelta(days=7)
default_end = today 

date = st.date_input(
    "Date Range",
    value=(default_start, default_end),
    max_value=end_date,
    format="MM.DD.YYYY",
)

region = st.selectbox("Focused Region", ["Southeast Asia & India", "Greater China", "North America", "Europe", "Middle East & Africa (EMEA)", "Asia Pacific & latin America (ALPA)", "Thailand", "India" ])

col1, col2 = st.columns([3, 1])

with col1:
    if st.button("Run Competitor Analysis"):
        if all([company_name, competitor_names, date, region]):
            printer = Printer()
            with st.spinner("Running analysis..."):
                printer.update_item("research", "Starting research...", is_done=False)
                try:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    start_date, end_date = date
                    date_range = f"{start_date.strftime('%B %d, %Y')} to {end_date.strftime('%B %d, %Y')}"
                    research_manager = AiManager(company_name, ', '.join(competitor_names), date_range, region, printer)
                    output = loop.run_until_complete(research_manager.run_crews())
                    result = output.full_report
                    report_filename = output.file_name
                    report_path = os.path.join(REPORT_DIR, report_filename)

                    # 🟢 Store in session_state before rerun
                    st.session_state["new_report"] = report_filename

                    printer.mark_item_done("research")
                    printer.update_item("result", "Report generated successfully!", is_done=True)
                    st.success("Analysis complete! Check the reports list.")
                    show_confetti()
                    st.rerun()
                except Exception as e:
                    printer.update_item("error", f"Error: {str(e)}", is_done=True)
                    st.error(f"Error during analysis: {e}")
        else:
            st.warning("Please fill in all fields!")

with col2:
    if selected_report and selected_report != "No reports match your filters":
        pdf_path = os.path.join(REPORT_DIR, selected_report.replace(".md", ".pdf"))
        get_pdf_download_link(pdf_path, selected_report.replace(".md", ".pdf"))

if selected_report and selected_report != "No reports match your filters":
    with open(os.path.join(REPORT_DIR, selected_report), "r") as f:
        report_content = f.read()
    report_content = report_content.replace("![Chart](temp/", "*Please download PDF file to view the chart*  ---> ![Chart](temp/")
    st.divider()
    st.markdown(report_content, unsafe_allow_html=True)
elif selected_report == "No reports match your filters":
    st.info("No reports match your selected filters. Please adjust your filter criteria or generate a new report.")

st.markdown(
    """
    <style>
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 16px;
        color: #333;
    }

    h1, h2, h3 {
        color: #1f2e4d;
        font-weight: 600;
    }

    .stDownloadButton > button {
        width: auto;
        background-color: #0052cc;
        color: #ffffff;
        border: none;
        border-radius: 6px;
        padding: 10px 24px;
        font-size: 14px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }

    .stDownloadButton > button:hover {
        background-color: #003d99;
        color: #ffffff;
    }

    .stButton > button {
        background-color: #28a745;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 10px 24px;
        font-size: 14px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }

    .stButton > button:hover {
        background-color: #218838;
        color: white;
    }

    .stSidebar {
        background-color: #f1f3f6;
    }

    .stProgress .st-bo {
        background-color: #28a745;
    }

    .st-emotion-cache-179n174 {
        display: block;
    }
    </style>
    """,
    unsafe_allow_html=True
)
