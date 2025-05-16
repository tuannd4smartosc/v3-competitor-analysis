import streamlit as st
import os
from datetime import datetime
import asyncio
from dotenv import load_dotenv
from manager import ResearchManager  # Your async research manager
from config import REPORT_DIR  # Assuming REPORT_DIR is defined in config
from utils import show_confetti, markdown_to_pdf, get_pdf_download_link, sort_file_names  # Keep these utilities
from user_prompt import generate_prompt
from st_printer import Printer
import datetime
from streamlit_tags import st_tags

# Load environment variables (e.g., API keys)
load_dotenv()

# Streamlit configuration
st.set_page_config(page_title="Nike's Competitors Analysis Dashboard", layout="wide", initial_sidebar_state="expanded")

# Sidebar for report filtering
st.sidebar.title("Reports")
if not os.path.exists(REPORT_DIR):
    os.makedirs(REPORT_DIR)

report_files = [f for f in os.listdir(REPORT_DIR) if f.endswith(".md")]

md_reports = sort_file_names(report_files)
selected_report = st.sidebar.selectbox("Select a Report", md_reports)

# Main dashboard
st.title("Nike's Competitor Analysis Dashboard")
st.markdown("Analyze Nike's competitor pricing and promotions with a single click!")

# Input fields for analysis
# company_name = st.text_input("Your Company's Name", placeholder="e.g., Acme Corp", value="Nike")
company_name = "Nike"

default_competitors = [
    "Adidas", "Levis", "New Balance", "Lululemon", "Puma",
    "Sketchers", "Under Armour", "Reebok", "ASICS", "Fila"
]

competitor_names = st_tags(
    label="Competitor Names",
    text="Type a name and press enter",
    value=[],
    suggestions=default_competitors,
    maxtags=15,
    key="competitor_tags"
)

today = datetime.date.today()
start_date = today
end_date = today.replace(year=today.year + 5)

default_start = today
default_end = today + datetime.timedelta(days=365)

date = st.date_input(
    "Date Range",
    value=(default_start, default_end),
    max_value=end_date,
    format="MM.DD.YYYY",
)

region = st.selectbox("Focused Regions", ["Greater China", "North America", "Europe", "Middle East & Africa (EMEA)", "Asia Pacific & latin America (ALPA)" ])

# Button to run analysis
if st.button("Run Competitor Analysis"):
    if all([company_name, competitor_names, date, region]):
        printer = Printer()
        query = generate_prompt(company_name, competitor_names, date, region)
        printer.update_item("query", "Generated query: " + query[:100] + "...", is_done=True)

        with st.spinner("Running analysis..."):
            printer.update_item("research", "Starting research...", is_done=False)
            try:
                # Run ResearchManager asynchronously
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                manager_id = f"{company_name}_ca_{date}_{region}"
                research_manager = ResearchManager(manager_id, printer)
                result = loop.run_until_complete(ResearchManager(manager_id, printer).run(query))
                printer.mark_item_done("research")
                report_filename = research_manager.file_name
                report_path = os.path.join(REPORT_DIR, report_filename)
                selected_report = report_path
                printer.update_item("result", "Report generated successfully!", is_done=True)
                st.success("Analysis complete! Check the reports list.")
                show_confetti()
                st.rerun()  # Refresh to update report list
            except Exception as e:
                printer.update_item("error", f"Error: {str(e)}", is_done=True)
                st.error(f"Error during analysis: {e}")
    else:
        st.warning("Please fill in all fields!")

# Display selected report
if selected_report:
    with open(os.path.join(REPORT_DIR, selected_report), "r") as f:
        report_content = f.read()
    st.divider()
    st.markdown(report_content, unsafe_allow_html=True)

    pdf_path = os.path.join(REPORT_DIR, selected_report.replace(".md", ".pdf"))
    st.markdown(get_pdf_download_link(pdf_path, selected_report.replace(".md", ".pdf")), unsafe_allow_html=True)

# Custom CSS (unchanged from your code)
st.markdown(
    """
    <style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        transition: background-color 0.3s;
    }
    .stButton>button:hover {
        background-color: #ffffff;
        color: #4CAF50;
        border: 1px solid #4CAF50;
    }
    .stSidebar {
        background-color: #f8f9fa;
    }
    .stProgress .st-bo {
        background-color: #4CAF50;
    }
    body {
        font-family: 'Arial', sans-serif;
    }
    h1, h2, h3 {
        color: #2c3e50;
    }
    </style>
    """,
    unsafe_allow_html=True
)