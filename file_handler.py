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
