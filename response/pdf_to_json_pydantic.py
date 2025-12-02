from PyPDF2 import PdfReader
from pydantic import BaseModel
from typing import List
from openai import OpenAI
from dotenv import load_dotenv
import os


load_dotenv()
api_key = os.getenv("API_KEY")
client = OpenAI(api_key=api_key)

# PyPDF2 output: pdf to text
reader = PdfReader("../data/invoices_pdf/202501-invoice.pdf")
page = reader.pages[0]
text = page.extract_text()


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


# details_schema = details.model_json_schema()

# call ai request json formatted output of invoice details
prompt = f"Please extract the invoice number, invoice date, product number, description, quantity, unit price, and amount from {text}. Format as json."
response = client.responses.parse(model="gpt-5-nano", input=prompt, text_format=Invoice)
print(response.output_text)
