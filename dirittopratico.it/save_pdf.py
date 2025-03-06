from fpdf import FPDF
from bs4 import BeautifulSoup
import re

class PDF(FPDF):
    def header(self):
        self.set_font("Courier", "B", 16, uni=True)

    def footer(self):
        self.set_y(-15)
        self.set_font("Courier", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

def extract_text_from_html(html_content):
    soup = BeautifulSoup(html_content, "html.parser")

    # Remove elements like <span class="omissis"> and replace with ###
    for span in soup.find_all("span", class_="omissis"):
        span.replace_with("###")

    # Convert HTML elements to plain text
    for tag in soup.find_all(True):  
        if "center" not in tag.get("class", []):
            tag.replace_with(tag.get_text())

    return soup.get_text(separator="\n")

def create_pdf(title, content):
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Courier", "B", 16, uni=True)

    # Title Formatting
    title_parts = title.split(",")
    title_part1 = title_parts[0]
    title_part2 = title_parts[1] if len(title_parts) > 1 else ""

    pdf.cell(0, 10, title_part1.strip(), ln=True, align="C")
    pdf.set_font("Courier", "", 12, uni=True)
    pdf.cell(0, 10, title_part2.strip(), ln=True, align="C")

    pdf.ln(10)  # Line break

    # Content Formatting
    pdf.set_font("Courier", "", 10, uni=True)
    max_width = pdf.w - 40
    for line in str(content).split("\n"):
        pdf.multi_cell(max_width, 5, line)

    pdf.ln(10)

    # Permalink
    # pdf.set_font("Helvetica", "I", 8)
    # pdf.cell(0, 10, f"Non-official copy available at:", ln=True)
    # pdf.set_text_color(0, 0, 255)
    # pdf.cell(0, 10, permalink, ln=True, link=permalink)

    # Save the PDF
    sanitized_title = re.sub(r"[\/:*?\"<>|]", "-", title)
    pdf.output(f"output/{sanitized_title}.pdf", "F", encoding="utf-8")

# Example usage:
html_content = """
<div class='provvedimento'>
    <h3>Sample Title, Example Subtitle</h3>
    <div class='contenuto'>
        <pre>
            This is some sample content.
            <span class="omissis">Hidden Text</span>
            More text.
        </pre>
    </div>
    <button data-permalink="https://example.com/document"></button>
</div>
"""

title = "Sample Title, Example Subtitle"
# permalink = "https://example.com/document"
# content = extract_text_from_html(html_content)

# create_pdf(title, content)
