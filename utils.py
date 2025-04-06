import re
import streamlit as st
from markdown import markdown
import json
import os
from weasyprint import HTML

def show_confetti():
    st.balloons()

def markdown_to_pdf(markdown_text, output_path):
    html_text = markdown(markdown_text, extensions=['markdown.extensions.tables', 'markdown.extensions.extra', 'markdown.extensions.nl2br'])
    styled_html = f"""
    <body>
        <style>
            body {{ font-family: Arial, sans-serif; color: #333; margin: 0; padding: 20px;}}
            .report-container {{ max-width: 800px; margin: 0 auto; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); }}
            h1, h2, h3 {{ color: #2c3e50; }}
            table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
            th, td {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
            th {{ background-color: #f4f4f4; color: #2c3e50; font-weight: bold; }}
            td {{ background-color: #fff; }}
            tr:nth-child(odd) td {{ background-color: #f9f9f9; }}
            p, li {{ line-height: 1.6; margin: 10px 0; }}
            ol {{ padding-left: 20px; }}
        </style>
        <div class="report-container">
            {html_text}
        </div>
    </body>
    </html>
    """
    
    HTML(string=styled_html).write_pdf(output_path)

def get_pdf_download_link(pdf_path, filename):
    with open(pdf_path, "rb") as f:
        pdf_data = f.read()
    return st.download_button(
        label="Download PDF",
        data=pdf_data,
        file_name=filename,
        mime="application/pdf",
    )

def extract_timestamp(filename):
    name_part = os.path.splitext(filename)[0]  
    parts = name_part.split("-")             
    timestamp = parts[-1]                     
    return timestamp

def sort_file_names(file_names: list[str]):
    sorted_files = sorted(file_names, key=extract_timestamp, reverse=True)
    return sorted_files