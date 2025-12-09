from dotenv import load_dotenv
import os
import shipping_list_processing as ship
import utils


load_dotenv()
api_key = os.getenv("API_KEY")


# Shipping List Batch Loader
# This script will insert all invoice pdfs in this directory into the database:
data_dir = r"../data/shipping_lists_pdf"

# Iterate over files in directory
for name in os.listdir(data_dir):
    # Open file
    with open(os.path.join(data_dir, name)) as f:
        print(f"Loading Filename: '{name}'")
        # Assemble paths
        pdf_doc = name
        pdf_path = data_dir + "/" + pdf_doc
        db_dir = "../db/"
        db_file = "shipping_lists.db"
        db_path = db_dir + db_file

        print(f"pdf_path = {pdf_path}")
        # Check if pdf document exists, if not, exit
        if not os.path.exists(pdf_path):
            print(f"❌ PDF not found: {pdf_path}")
            exit(1)
        # Ask LLM if the document is a shipping list
        if utils.classify(pdf_path, api_key) == "shipping list":
            print("Shipping List Detected. Waiting on LLM Response.")
            pdf_text = ship.pdf_reader(pdf_path)
            # print(pdf_text)
            # Request pdf data as a structured output JSON response from LLM
            json_response = ship.structured_output(pdf_text, api_key)
            print("JSON response requested.")
            ship.save_to_sqlite(json_response, db_path)
        else:
            print("The document does not appear to be a shipping list.")
