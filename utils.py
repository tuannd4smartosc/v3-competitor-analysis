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
            @page {{
                size: A4 landscape;
                margin: 2cm;
            }}

            body {{
                font-family: "Georgia", serif;
                color: #2a2a2a;
                line-height: 1.6;
                font-size: 12pt;
                background: white;
            }}

            h1, h2, h3, h4 {{
                font-family: "Helvetica Neue", sans-serif;
                color: #003366;
                margin-top: 1.5em;
                margin-bottom: 0.5em;
            }}

            h1 {{
                font-size: 22pt;
                border-bottom: 2px solid #003366;
                padding-bottom: 0.3em;
            }}

            h2 {{
                font-size: 18pt;
                border-left: 4px solid #003366;
                padding-left: 10px;
            }}

            h3 {{
                font-size: 16pt;
                color: #0055aa;
            }}

            h4 {{
                font-size: 14pt;
                color: #336699;
            }}

            p {{
                margin: 0 0 1em 0;
                text-align: justify;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 1.5em 0;
                font-size: 11pt;
            }}

            th, td {{
                border: 1px solid #dddddd;
                text-align: left;
                padding: 8px;
            }}

            th {{
                background-color: #f2f2f2;
                font-weight: bold;
                color: #003366;
            }}

            tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}

            code {{
                background: #f4f4f4;
                padding: 2px 4px;
                font-size: 10pt;
                border-radius: 4px;
            }}

            ul, ol {{
                margin: 0 0 1em 1.5em;
            }}

            .page-break {{
                page-break-before: always;
            }}

            .footer {{
                text-align: center;
                font-size: 9pt;
                color: #999999;
                margin-top: 3em;
            }}

            blockquote {{
                border-left: 4px solid #cccccc;
                padding-left: 1em;
                font-style: italic;
                color: #555555;
            }}
        </style>
        <div class="report-container">
            {html_text}
        </div>
    </body>
    </html>
    """
    print(">>>>>>>>>>>>>>> styled_html",styled_html)
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