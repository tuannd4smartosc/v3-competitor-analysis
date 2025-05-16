from weasyprint import HTML
from markdown import markdown
from datetime import datetime
import os
from config import REPORT_DIR

def export_pdf(markdown_content):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    html_content =  markdown(markdown_content, extensions=['markdown.extensions.tables', 'markdown.extensions.extra', 'markdown.extensions.nl2br'])
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
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
    </head>
    <body>
    
    <div class="report-container">
        {html_content}
    </div>
    </body>
    </html>
    """

    # Convert to PDF using WeasyPrint
    HTML(string=html_template).write_pdf(f"output_file-{timestamp}.pdf")


def export_md(markdown_content, output_filename):
    os.makedirs(REPORT_DIR, exist_ok=True)
    file_path = os.path.join(REPORT_DIR, output_filename)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)
