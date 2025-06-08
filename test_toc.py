from utils import markdown_to_pdf
import os

# Test function with external Markdown file
if __name__ == "__main__":
    input_md_path = "reports/report-Adidas, Puma, Sketchers-Southeast Asia-June 01, 2025 to June 08, 2025-92272718b888474b88b7970c682cdec3.md"  # Relative path to your .md file
    output_pdf_path = "tests/output_test_new.pdf"

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)

    # Read markdown file
    with open(input_md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    # Generate PDF
    markdown_to_pdf(md_text, output_pdf_path)

    if os.path.exists(output_pdf_path):
        print(f"✅ PDF created successfully at: {output_pdf_path}")
    else:
        print("❌ Failed to create PDF.")
