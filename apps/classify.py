from PyPDF2 import PdfReader

# from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os

# PyPDF2 output: pdf to text
reader = PdfReader("../data/202501-invoice.pdf")
page = reader.pages[0]
text = page.extract_text()

load_dotenv()
api_key = os.getenv("API_KEY")
client = OpenAI(api_key=api_key)

# call ai request classification of the document
prompt = f"Please read the following document and determine what type of document this is. Return only one of the following strings: 'invoice', 'shipping list', or 'other'. Only return the string, do not add any other comments. Here is the document: {text}"
response = client.responses.create(model="gpt-4o", input=prompt)
print(response.output_text)
