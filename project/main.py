from dotenv import load_dotenv
import os
import invoice_processing as inv

load_dotenv()
api_key = os.getenv("API_KEY")


pdf_dir = "../data/invoices_pdf/"  # Update path to your PDF
pdf_doc = "202502-invoice.pdf"
pdf_path = pdf_dir + pdf_doc
db_dir = "../db/"
db_file = "invoices.db"
db_path = db_dir + db_file

print(f"pdf_path = {pdf_path}")

if not os.path.exists(pdf_path):
    print(f"❌ PDF not found: {pdf_path}")
    exit(1)

if inv.classify(pdf_path, api_key) == "invoice":
    # print("invoice detected")
    pdf_text = inv.pdf_reader(pdf_path)
    #    print(pdf_text)

    json_response = inv.structured_output(pdf_text, api_key)
    print("JSON response requested.")
    inv.save_to_sqlite(json_response, db_path)
    print("Database Connection Closed.")
