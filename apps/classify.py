from PyPDF2 import PdfReader
from openai import OpenAI
from dotenv import load_dotenv
import os

# PyPDF2 output: pdf to text
reader = PdfReader("../data/invoices_pdf/202501-invoice.pdf")
page = reader.pages[0]
text = page.extract_text()

load_dotenv()
api_key = os.getenv("API_KEY")
client = OpenAI(api_key=api_key)

# call ai request classification of the document
prompt = f"Please read the following document and determine what type of document this is. Return only one of the following strings: 'invoice', 'shipping list', or 'other'. Only return the string, do not add any other comments. Here is the document: {text}"
response = client.responses.create(model="gpt-5-nano", input=prompt)
print(response.output_text)
print(f"Here is the text: \n{text}")
