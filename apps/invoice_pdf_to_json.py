from PyPDF2 import PdfReader
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os


load_dotenv()
api_key = os.getenv("API_KEY")
client = OpenAI(api_key=api_key)

# PyPDF2 output: pdf to text
reader = PdfReader("../data/202501-invoice.pdf")
page = reader.pages[0]
text = page.extract_text()


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

# call ai request json formatted output of invoice details
prompt = f"Please extract the invoice number, invoice date, product number, description, quantity, unit price, and amount from {text}. Format as json."
response = client.responses.create(model="gpt-4o", input=prompt)
print(response.output_text)
