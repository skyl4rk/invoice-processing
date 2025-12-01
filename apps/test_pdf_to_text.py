# from pypdf2 import pdfreader
from PyPDF2 import PdfReader
import fitz
import pdfplumber
from openai import OpenAI
import json
from dotenv import load_dotenv
import os
from docling.document_converter import DocumentConverter


load_dotenv()
api_key = os.getenv("API_KEY")

client = OpenAI(api_key=api_key)

pdf_path = "../data/invoices_pdf/202501-invoice.pdf"

"""
This script takes a pdf document and outputs text, markdown or json from a number of python packages which process pdf to text. The results are in the output directory.
"""

print("#-----------------")
print("Begin PyPDF2:")

reader = PdfReader(pdf_path)
# print(str(len(reader.pages)) + " pages")
page = reader.pages[0]
text = page.extract_text()
# print(text)

# Save to file
output_file = "../output/PyPDF2.txt"
with open(output_file, "w") as f:
    f.write(text)

print("End PyPDF2.")

print("#-----------")
print("Begin fitz:")
file = fitz.open(pdf_path)
for page in file:
    text2 = page.get_text()
# print(text2)

# Save to file
output_file = "../output/Fitz.txt"
with open(output_file, "w") as f:
    f.write(text2)

print("End fitz.")

print("#----------------")
print("Begin pdfplumber:")

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        pdf_text = page.extract_text()
        output_file = "../output/Pdfplumber.txt"
        with open(output_file, "a") as f:
            f.write(pdf_text)

print("End pdfplumber.")

print("#-----------")
print("Begin docling:")

# source = pdf_path
converter = DocumentConverter()
result = converter.convert(pdf_path)

# Export to markdown
markdown_content = result.document.export_to_markdown()

# Save to file
output_file = "../output/DoclingMarkdown.md"
with open(output_file, "w") as f:
    f.write(markdown_content)

print("Docling Markdown:")
print(f"Successfully converted {pdf_path} to {output_file}")

output_json_file = "../output/DoclingStructure.json"
with open(output_json_file, "w") as f:
    json.dump(result.document.export_to_dict(), f, indent=2)

print(f"Successfully exported structure to {output_json_file}")
