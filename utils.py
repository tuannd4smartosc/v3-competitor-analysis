import re
import streamlit as st
from markdown import markdown
import json
import os
from weasyprint import HTML

def show_confetti():
    st.balloons()

def generate_title_from_markdown(markdown_text):
    match = re.search(r'^#\s+(.*)', markdown_text, re.MULTILINE)
    if match:
        title = match.group(1).strip()
        markdown_text = markdown_text.replace(match.group(0), '', 1).lstrip()
        return title
    return "Untitled Report", markdown_text


def generate_toc_from_markdown(markdown_text):
    toc_entries = []
    modified_lines = []

    header_index = 0

    for line in markdown_text.splitlines():
        heading_match = re.match(r'^(#{2,3})\s+(.*)', line)
        if heading_match:
            hashes, title = heading_match.groups()
            level = len(hashes)
            anchor_id = f'section-{header_index}'
            indent = '  ' * (level - 1)
            toc_entries.append(f'{indent}<li style="margin-left: {(level - 1) * 1}em; list-style-type: none;"><span style="font-family: "Georgia", serif; all: unset; font-size: 12pt;"><a href="#{anchor_id}" style="color:#2a2a2a;text-decoration: none">{title}</a></span></li>')
            line = f'{hashes} <a id="{anchor_id}"></a>{title}'
            header_index += 1

        modified_lines.append(line)

    toc_html = "<div class='toc'><h2>Table of Contents</h2>\n<ul>\n" + "\n".join(toc_entries) + "\n</ul>\n</div>\n<div style='page-break-after: always;'></div>"
    updated_markdown = "\n".join(modified_lines)

    return toc_html, updated_markdown

def markdown_to_pdf(markdown_text, output_path):
    toc_html, updated_markdown = generate_toc_from_markdown(markdown_text)
    title_html = generate_title_from_markdown(markdown_text)

    html_text = markdown(updated_markdown + "\n\n", extensions=['markdown.extensions.tables', 'markdown.extensions.extra', 'markdown.extensions.nl2br'])
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
            .cover {{
                display: flex;
                height: 90vh;
                align-items: center;
                justify-content: center;
                text-align: center;
                font-size: 28pt;
                font-weight: bold;
                color: #003366;
                page-break-after: always;
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
        <div class="cover">{title_html}</div>
        {toc_html}
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