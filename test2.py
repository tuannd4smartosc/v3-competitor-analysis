
from utils import markdown_to_pdf

with open("reports/test-report.md", "r", encoding="utf-8") as f:
    content = f.read()
    print("content",content)
    markdown_to_pdf(content, "test-pdf3.pdf")