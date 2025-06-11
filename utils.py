import glob
import html
import re
import shutil
import unicodedata
import streamlit as st
from markdown import markdown
import json
import os
from weasyprint import HTML
import csv
import io

from _agents.search import APAWebReference
from config import REPORT_DIR

def show_confetti():
    st.balloons()

def slugify(text):
    """Creates a URL-safe slug from a heading title."""
    text = unicodedata.normalize("NFKD", text)
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    return re.sub(r"[-\s]+", "-", text)

def generate_title_from_markdown(markdown_text, include_title_in_toc=False):
    match = re.search(r'^#\s+(.*)', markdown_text, re.MULTILINE)
    if match:
        title = match.group(1).strip()
        if not include_title_in_toc:
            markdown_text = markdown_text.replace(match.group(0), '', 1).lstrip()
        return title, markdown_text
    return "Nike Competitor Analysis", markdown_text

def generate_toc_from_markdown(markdown_text):
    toc_entries = []
    modified_lines = []

    used_ids = set()

    for line in markdown_text.splitlines():
        heading_match = re.match(r'^(#{2,6})\s+(.*)', line)
        if heading_match:
            hashes, raw_title = heading_match.groups()
            level = len(hashes)

            clean_title = re.sub(r'\*\*(.*?)\*\*|__(.*?)__|\*(.*?)\*|`(.*?)`', r'\1\2\3\4', raw_title)
            escaped_title = html.escape(clean_title.strip())

            # Generate unique anchor_id from slug
            base_slug = slugify(clean_title)
            anchor_id = base_slug
            suffix = 1
            while anchor_id in used_ids:
                anchor_id = f"{base_slug}-{suffix}"
                suffix += 1
            used_ids.add(anchor_id)

            # Format heading line with anchor
            line = f'{hashes} <a id="{anchor_id}"></a>{raw_title}'

            # Format ToC entry
            indent = '  ' * (level - 1)
            formatted_title = f'<strong>{escaped_title}</strong>' if level == 2 else escaped_title
            toc_entries.append(
                f'{indent}<li style="margin-left: {(level - 1) * 1}em; list-style-type: none;">'
                f'<span style="font-family: Georgia, serif; all: unset; font-size: 12pt;">'
                f'<a href="#{anchor_id}" style="color:#2a2a2a;text-decoration: none">{formatted_title}</a>'
                f'</span></li>'
            )

        modified_lines.append(line)

    toc_html = (
        "<div class='toc'><h2>Table of Contents</h2>\n<ul>\n"
        + "\n".join(toc_entries)
        + "\n</ul>\n</div>\n<div style='page-break-after: always;'></div>"
    )
    updated_markdown = "\n".join(modified_lines)

    return toc_html, updated_markdown

def markdown_to_pdf(markdown_text, output_path):
    toc_html, updated_markdown = generate_toc_from_markdown(markdown_text)
    title_html, md_text = generate_title_from_markdown(markdown_text)

    html_text = markdown(updated_markdown + "\n\n", extensions=['markdown.extensions.tables', 'markdown.extensions.extra'])
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
    with open("report.html", "w", encoding="utf-8") as file:
        file.write(styled_html)
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


def export_md(markdown_content, output_filename):
    os.makedirs(REPORT_DIR, exist_ok=True)
    file_path = os.path.join(REPORT_DIR, output_filename)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)
        
def generate_csv_file_from_text(csv_text, output_filename):
    """
    Generates a CSV file from a CSV formatted string.

    Args:
        csv_text (str): A string containing CSV data.
        output_filename (str): The name of the CSV file to be created.
    """
    try:
        # Use StringIO to treat the string as a file
        csv_file_in_memory = io.StringIO(csv_text)

        # Create a CSV reader from the in-memory file
        reader = csv.reader(csv_file_in_memory)

        # Open the output CSV file in write mode
        with open(output_filename, 'w', newline='', encoding='utf-8') as outfile:
            # Create a CSV writer for the output file
            writer = csv.writer(outfile)

            # Write each row from the in-memory reader to the output file
            for row in reader:
                writer.writerow(row)
        print(f"CSV file '{output_filename}' generated successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
        
        

def convert_dict_to_csv_text_for_campaigns(data_dict):
    """
    Converts a nested Python dictionary into a CSV formatted string.

    Args:
        data_dict (dict): The input dictionary, potentially with nested structures.

    Returns:
        str: A string containing the CSV formatted data.
    """

    # Define the mapping for old column names to new desired names
    # The key is the original flattened path, value is the new column header
    column_name_map = {
        'search_result_item_search_result': 'Promotion campaign summary',
        'search_result_item_url': 'URL',
        'metadata_date_range': 'Date range applied for search',
        'metadata_country_code': 'Country',
        'metadata_search_type': 'Search type'
    }

    # Flatten the dictionary and apply new column names
    flattened_data = {}

    # Process 'search_result_item'
    if 'search_result_item' in data_dict:
        sri = data_dict['search_result_item']
        flattened_data[column_name_map.get('search_result_item_search_result', 'search_result_item_search_result')] = sri.get('search_result')
        flattened_data['search_result_item_has_promotion_campaign'] = sri.get('has_promotion_campaign')
        flattened_data['search_result_item_relativity_score'] = sri.get('relativity_score')
        flattened_data[column_name_map.get('search_result_item_url', 'search_result_item_url')] = sri.get('url')
        flattened_data['search_result_item_need_deep_dive'] = sri.get('need_deep_dive')

    # Process 'metadata'
    if 'metadata' in data_dict:
        meta = data_dict['metadata']
        flattened_data['metadata_query'] = meta.get('query')
        flattened_data[column_name_map.get('metadata_date_range', 'metadata_date_range')] = meta.get('date_range')
        flattened_data[column_name_map.get('metadata_country_code', 'metadata_country_code')] = meta.get('country_code')
        flattened_data[column_name_map.get('metadata_search_type', 'metadata_search_type')] = meta.get('search_type')

    # Ensure all values are strings for CSV writing, especially booleans or numbers
    for key, value in flattened_data.items():
        if value is not None:
            flattened_data[key] = str(value)
        else:
            flattened_data[key] = '' # Handle None values as empty strings

    # Prepare for CSV writing
    # Use io.StringIO to write to an in-memory text buffer
    output_buffer = io.StringIO()

    # Get the fieldnames (column headers) from the flattened dictionary keys
    fieldnames = list(flattened_data.keys())

    # Create a CSV DictWriter object
    # writerow expects a dictionary where keys match fieldnames
    csv_writer = csv.DictWriter(output_buffer, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)

    # Write the header row
    csv_writer.writeheader()

    # Write the data row
    csv_writer.writerow(flattened_data)

    # Get the CSV string from the buffer
    csv_string = output_buffer.getvalue()

    return csv_string