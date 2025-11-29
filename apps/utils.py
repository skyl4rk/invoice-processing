from PyPDF2 import PdfReader
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os


load_dotenv()
api_key = os.getenv("API_KEY")
client = OpenAI(api_key=api_key)


# PyPDF2 output: pdf to text, process first page of pdf
def pdf_to_text(pdf_document):
    reader = PdfReader(pdf_document)
    page = reader.pages[0]
    text = page.extract_text()
    return text


# call ai request classification of the document
def doc_type(text):
    prompt = f"Please read the following document and determine what type of document this is. Return only one of the following strings: 'invoice', 'shipping list', or 'other'. Only return the string, do not add any other comments. Here is the document: {text}"
    response = client.responses.create(model="gpt-4o", input=prompt)
    print(f"The document is: {response.output_text}")
    return response.output_text


# call ai request json formatted output of invoice details
def invoice_extract_data(text_doc):
    prompt = f"Please extract the invoice number, invoice date, product number, description, quantity, unit price, and amount from {text_doc}. Format as json."
    response = client.responses.create(model="gpt-4o", input=prompt)
    print(response.output_text)
    return response.output_text


# pydantic structured output schema
class details(BaseModel):
    invoice_number: int
    invoice_date: str
    product_number: int
    description: str
    quantity: int
    unit_price: float
    amount: float


details_schema = details.model_json_schema()
# --------------------

path_to_pdf = "../data/202501-invoice.pdf"

if doc_type(pdf_to_text(path_to_pdf)) == "invoice":
    json_output = invoice_extract_data(pdf_to_text(path_to_pdf))
