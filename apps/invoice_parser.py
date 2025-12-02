from PyPDF2 import PdfReader
from pydantic import BaseModel, ValidationError
from typing import List
from openai import OpenAI
import sqlite3
from dotenv import load_dotenv
import os


load_dotenv()
api_key = os.getenv("API_KEY")
client = OpenAI(api_key=api_key)


def pdf_reader(doc_path):
    # PyPDF2 output: pdf to text
    reader = PdfReader(doc_path)
    page = reader.pages[0]
    text = page.extract_text()
    return text


def structured_output(payload):
    # Pydantic models for structured output
    class Product(BaseModel):
        product_number: str
        description: str
        quantity: int
        unit_price: float
        amount: float

    class Invoice(BaseModel):
        invoice_number: str
        invoice_date: str
        products: List[Product]
        total: float

    # call ai request json formatted output of invoice details
    prompt = f"Please extract the invoice number, invoice date, product number, description, quantity, unit price, and amount from {payload}. Format as json."
    response = client.responses.parse(
        model="gpt-5-nano", input=prompt, text_format=Invoice
    )
    # print(response.output_text)
    return response.output_text


if __name__ == "__main__":
    path_to_invoice = "../data/invoices_pdf/202501-invoice.pdf"
    pdf_text = pdf_reader(path_to_invoice)
    json_response = structured_output(pdf_text)
    print(json_response)
