from PyPDF2 import PdfReader
from openai import OpenAI
from dotenv import load_dotenv
import os


load_dotenv()
api_key = os.getenv("API_KEY")
#    client = OpenAI(api_key=api_key)


def classify(doc, key):
    # PyPDF2 output: pdf to text
    reader = PdfReader(doc)
    page = reader.pages[0]
    text = page.extract_text()
    # call ai request classification of the document
    prompt = f"Please read the following document and determine what type of document this is. Return only one of the following strings: 'invoice', 'shipping list', or 'other'. Only return the string, do not add any other comments. Here is the document: {text}"

    client = OpenAI(api_key=key)
    response = client.responses.create(model="gpt-5-nano", input=prompt)
    #    print(response.output_text)
    return response.output_text


def pdf_reader(doc_path):
    # PyPDF2 output: pdf to text
    reader = PdfReader(doc_path)
    page = reader.pages[0]
    text = page.extract_text()
    return text


# This function is a placeholder and is not functional.
def process_files(dir):
    # Assign directory
    dir = r"../data/invoices_pdf"

    # Iterate over files in directory
    for name in os.listdir(dir):
        # Open file
        with open(os.path.join(dir, name)) as f:
            print(f"Filename: '{name}'")
            # Read content of file
            # pdf_file = f.read()
