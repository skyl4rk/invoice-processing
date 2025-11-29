from PyPDF2 import PdfReader

# from pydantic import BaseModel, ValidationError, Field
# from typing import List
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import jsonschema
import sqlite3


load_dotenv()
api_key = os.getenv("API_KEY")
client = OpenAI(api_key=api_key)


# PyPDF2 output: pdf to text, process first page of pdf
def pdf_to_text(pdf_document):
    reader = PdfReader(pdf_document)
    page = reader.pages[0]
    text = page.extract_text()
    print("pdf_to_text completed.")
    return text


# call ai request classification of the document
def doc_type(text):
    prompt = f"Please read the following document and determine what type of document this is. Return only one of the following strings: 'invoice', 'shipping list', or 'other'. Only return the string, do not add any other comments. Here is the document: {text}"
    response = client.responses.create(model="gpt-4o", input=prompt)
    print(f"The document is: {response.output_text}")
    print("doc_type completed.")
    return response.output_text


# call ai request json formatted output of invoice details
def invoice_extract_data(text_doc):
    prompt = f"Return only a JSON object, with no additional text. From the following text, extract the invoice number, invoice date, product number, description, quantity, unit price, and amount. Format as valid json. Do not include any other comments. Do not begin the response with ```. Do not include the text json. The text to process follows: {text_doc} "
    response = client.responses.create(model="gpt-4o", input=prompt)
    print(response.output_text)
    print("invoice_extract_data completed.")
    return response.output_text


def validateJSON(jsonData):
    try:
        json.loads(jsonData)
    except ValueError as err:
        print("Data not validated as JSON.")
        return False
    print("Data validated as JSON.")
    return True


path_to_pdf = "../data/202501-invoice.pdf"

if doc_type(pdf_to_text(path_to_pdf)) == "invoice":
    json_output = invoice_extract_data(pdf_to_text(path_to_pdf))

if validateJSON(json_output):
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect("../db/invoices.db")
    cursor = conn.cursor()

    # Create the invoices table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS invoices (
        invoice_number TEXT PRIMARY KEY,
        invoice_date TEXT,
        total REAL
    )
    """)

    # Create the products table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        product_number TEXT PRIMARY KEY,
        description TEXT,
        quantity INTEGER,
        unit_price REAL,
        amount REAL,
        invoice_number TEXT,
        FOREIGN KEY (invoice_number) REFERENCES invoices (invoice_number)
    )
    """)

    # Commit the changes
    conn.commit()

    # Insert the invoice data
    invoice_data = json.loads(json_output)
    cursor.execute(
        """
    INSERT INTO invoices (invoice_number, invoice_date, total)
    VALUES (?, ?, ?)
    """,
        (
            invoice_data["invoice_number"],
            invoice_data["invoice_date"],
            invoice_data["total"],
        ),
    )

    # Insert the product data
    for product in invoice_data["products"]:
        cursor.execute(
            """
        INSERT INTO products (product_number, description, quantity, unit_price, amount, invoice_number)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
            (
                product["product_number"],
                product["description"],
                product["quantity"],
                product["unit_price"],
                product["amount"],
                invoice_data["invoice_number"],
            ),
        )

    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()

"""
class Product(BaseModel):
    product_number: str
    description: str
    quantity: int
    unit_price: float
    amount: float


class Invoice(BaseModel):
    invoice_number: str
    invoice_date: str
    items: List[Product]
    total: float
"""
"""
# Try to parse the response text into the Pydantic model
try:
    # Ensure the response text is valid JSON
    test_output = json.loads(json_output)
except json.JSONDecodeError as e:
    print("JSON Decode Error:", e)
    test_output = {}


# Try to parse the response text into the Pydantic model
try:
    invoice_data = json.loads(json_output)
    invoice = Invoice(**invoice_data)
    print("Extracted Invoice Data:")
    print(invoice)
except ValidationError as e:
    print("Validation Error:", e)
except json.JSONDecodeError as e:
    print("JSON Decode Error:", e)
"""
