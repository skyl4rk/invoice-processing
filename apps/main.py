import os
from typing import List
import pandas as pd
import playground.invoice as inv


if __name__ == "__main__":
    pdf_path = "../data/invoices_pdf/202501-invoice.pdf"  # Update path to your PDF

    if not os.path.exists(pdf_path):
        print(f"❌ PDF not found: {pdf_path}")
        exit(1)

    try:
        text = inv.extract_pdf_text(pdf_path)

        print("text output:")
        print(text)

        invoice_data = inv.parse_invoice_with_ai(text)
        inv.save_to_sqlite(invoice_data)

        # Query to verify
        conn = inv.sqlite3.connect("../db/invoices.db")
        print("\n📊 Invoices table:")
        print(pd.read_sql_query("SELECT * FROM invoices", conn))
        print("\n📦 Products table:")
        print(pd.read_sql_query("SELECT * FROM products", conn))
        conn.close()
    except Exception as e:
        print(f"❌ Error: {e}")
