import glob
import re
import shutil
import streamlit as st
from markdown import markdown
import json
import os
from weasyprint import HTML

from _agents.search import APAWebReference

def show_confetti():
    st.balloons()

def generate_title_from_markdown(markdown_text):
    match = re.search(r'^#\s+(.*)', markdown_text, re.MULTILINE)
    if match:
        title = match.group(1).strip()
        markdown_text = markdown_text.replace(match.group(0), '', 1).lstrip()
        return title, markdown_text
    return "Nike Competitor Analysis", markdown_text


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
            
            if level == 2:
                title = f'<strong>{title}</strong>'
            else:
                title = title

            toc_entries.append(f'{indent}<li style="margin-left: {(level - 1) * 1}em; list-style-type: none;"><span style="font-family: "Georgia", serif; all: unset; font-size: 12pt;"><a href="#{anchor_id}" style="color:#2a2a2a;text-decoration: none">{title}</a></span></li>')
            line = f'{hashes} <a id="{anchor_id}"></a>{title}'
            header_index += 1

        modified_lines.append(line)

    toc_html = "<div class='toc'><h2>Table of Contents</h2>\n<ul>\n" + "\n".join(toc_entries) + "\n</ul>\n</div>\n<div style='page-break-after: always;'></div>"
    updated_markdown = "\n".join(modified_lines)

    return toc_html, updated_markdown

def markdown_to_pdf(markdown_text, output_path):
    toc_html, updated_markdown = generate_toc_from_markdown(markdown_text)
    title_html, md_text = generate_title_from_markdown(markdown_text)

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
            
            img {{
                max-width: 100%;
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
    print(">>>>>>>>>>>>>>> styled_html",styled_html)
    HTML(string=styled_html, base_url=os.getcwd() ).write_pdf(output_path)

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

def get_first_temp_filename(folder_path: str):

    files = sorted(f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)))

    if files:
        first_file = files[0]
        return first_file
    else:
        print("The folder is empty.")
        return None

def get_latest_file(folder_path):
    files = glob.glob(os.path.join(folder_path, '*'))  # All files
    if not files:
        return None
    latest_file = max(files, key=os.path.getmtime)
    return latest_file    

def empty_folder(folder_path: str):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.remove(file_path)  # Delete file or symbolic link
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # Delete folder and its contents
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')
            
def format_apa_citation(ref: APAWebReference) -> str:
    # Format the author
    author = ref.author if ref.author else ref.website_name
    # Format the year
    year = f"({ref.year})" if ref.year else "(n.d.)"
    # Format access date
    access_str = f"Accessed {ref.access_date.strftime('%B %d, %Y')}." if ref.access_date else ""
    # Combine into APA format
    citation = f"{author}. {year}. *{ref.title}*. {ref.website_name}. {access_str} [https://{ref.url.lstrip('https://')}]"
    return citation

def generate_citation_markdown(reference_list: list[APAWebReference]) -> str:
    citations = [format_apa_citation(ref) for ref in reference_list]
    markdown_text = "\n\n".join(citations)
    return markdown_text