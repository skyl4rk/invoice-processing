from dotenv import load_dotenv
import os
import invoice_processing as inv
import shipping_list_processing as ship
import utils

load_dotenv()
api_key = os.getenv("API_KEY")


pdf_dir = "../data/shipping_lists_pdf/"  # Update path to your PDF
pdf_doc = "2502-shipping-list.pdf"
pdf_path = pdf_dir + pdf_doc
db_dir = "../db/"
db_file = "shipping_lists.db"
db_path = db_dir + db_file

print(f"pdf_path = {pdf_path}")

if not os.path.exists(pdf_path):
    print(f"❌ PDF not found: {pdf_path}")
    exit(1)

document_type = utils.classify(pdf_path, api_key)

if document_type == "invoice":
    print("Invoice Detected.")
    pdf_text = utils.pdf_reader(pdf_path)
    print("PDF to Text Processed. Waiting on LLM Response.")
    json_response = inv.structured_output(pdf_text, api_key)
    print("JSON Structured Response Requested.")
    inv.save_to_sqlite(json_response, db_path)
    print("Database Connection Closed.")

if document_type == "shipping list":
    print("Shipping List Detected.")
    pdf_text = utils.pdf_reader(pdf_path)
    # print(pdf_text)
    print("PDF to Text Processed. Waiting on LLM Response.")
    json_response = ship.structured_output(pdf_text, api_key)
    # print(json_response)
    print("JSON Structured Response Requested.")
    ship.save_to_sqlite(json_response, db_path)
    print("Database Connection Closed.")

if document_type == "other":
    print("This file has not been detected as either an invoice or shipping list.")
