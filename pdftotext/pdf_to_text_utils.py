from PyPDF2 import PdfReader
import fitz
import pdfplumber
from docling.document_converter import DocumentConverter
from openai import OpenAI
import json
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")

client = OpenAI(api_key=api_key)

pdf_path = "../data/invoices_pdf/202501-invoice.pdf"

print("#-----------------")
print("Begin PyPDF2:")

reader = PdfReader(pdf_path)
# print(str(len(reader.pages)) + " pages")
page = reader.pages[0]
text = page.extract_text()
print(text)


def PyPDF2_run(pdf_path):
    print("#-----------------")
    print("Begin PyPDF2:")
    reader = PdfReader(pdf_path)
    page = reader.pages[0]
    PyPDF2_text = page.extract_text()
    print(PyPDF2_text)
    output_file = "../output/PyPDF2.txt"
    with open(output_file, "w") as f:
        f.write(PyPDF2_text)
    print("End PyPDF2.")
    print("")


def fitz_run(pdf_path):
    print("")
    print("#-----------")
    print("Begin fitz:")
    # "text", "block", "words", "html", "dict", "json", "rawdict", "text", "flags=fitz.TEXT_PRESERVE_WHITESPACE"
    fitz_file = fitz.open(pdf_path)
    for page in fitz_file:
        fitz_text = page.get_text(text)
    print(fitz_text)
    output_file = "../output/Fitz.txt"
    with open(output_file, "w") as f:
        f.write(fitz_text)
    print("End fitz.")
    print("")


def pdfplumber():
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            pdf_text = page.extract_text()
            # layout_text = page.extract_text(layout=True)
            # custom_tolerance_text = page.extract_text(x_tolerance=10, y_tolerance=5)
            # ratio_tolerance_text = page.extract_text(x_tolerance_ratio=1.5) # e.g., 1.5 times the font_size
            """
            words = page.extract_words(
            x_tolerance=2,
            y_tolerance=3,
            keep_blank_chars=True, # Include spaces as characters
            return_chars=True      # Include constituent characters for each word
        )   """
            """
            text_lines = page.extract_text_lines(layout=True, return_chars=False)
            print("\n--- Extracted Text Lines ---")
            for line in text_lines[:5]: # Print first 5 lines
            print(line)
            """
            print(pdf_text)
            output_file = "../output/Pdfplumber.txt"
            with open(output_file, "a") as f:
                f.write(pdf_text)
        print("End pdfplumber.")
        print("")
        print("#-----------")
        print("")
