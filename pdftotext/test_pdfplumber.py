import pdfplumber

pdf_path = "../data/invoices_pdf/202501-invoice.pdf"

# pdf_path = "../data/shipping_lists_pdf/2501-shipping-list.pdf"

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        pdf_text = page.extract_text()
        print("pdfplumber default:")
        print(pdf_text)
        output_file = "../output/Pdfplumber.txt"
        with open(output_file, "w") as f:
            f.write(pdf_text)
    print("End pdfplumber default.")
    print("")
    print("#-----------")
    print("")


with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        pdf_text = page.extract_text(layout=True)
        print("pdfplumber layout=True:")
        print(pdf_text)
        output_file = "../output/Pdfplumber.txt"
        with open(output_file, "a") as f:
            f.write(pdf_text)
    print("End pdfplumber layout=True.")
    print("")
    print("#-----------")
    print("")


with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        pdf_text = page.extract_text(layout=True, keep_blank_chars=True)
        print("pdfplumber layout=True, keep_blank_chars=True")
        print(pdf_text)
        output_file = "../output/Pdfplumber.txt"
        with open(output_file, "a") as f:
            f.write(pdf_text)
    print("End pdfplumber layout=True, keep_blank_chars=True.")
    print("")
    print("#-----------")
    print("")


with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        custom_tolerance_text = "x_tolerance=10, y_tolerance=5"
        pdf_text = page.extract_text(x_tolerance=10, y_tolerance=5)
        print(
            "pdfplumber custom_tolerance_text = page.extract_text(x_tolerance=10, y_tolerance=5):"
        )
        print(pdf_text)
        output_file = "../output/Pdfplumber.txt"
        with open(output_file, "a") as f:
            f.write(pdf_text)
    print("End pdfplumber custom_tolerance_text.")
    print("")
    print("#-----------")
    print("")


with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        ratio_tolerance_text = "x_tolerance_ratio=1.5"
        pdf_text = page.extract_text(x_tolerance_ratio=1.5)
        print("pdfplumber ratio_tolerance_text (x_tolerance_ratio=1.5):")
        print(pdf_text)
        output_file = "../output/Pdfplumber.txt"
        with open(output_file, "a") as f:
            f.write(pdf_text)
    print("End pdfplumber ratio_tolerance_text x_tolerance_ratio=1.5.")
    print("")
    print("#-----------")
    print("")


with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        words = "x_tolerance=2, y_tolerance=3, keep_blank_chars=True, return_chars=True"
        pdf_text = page.extract_text(
            x_tolerance=2, y_tolerance=3, keep_blank_chars=True, return_chars=True
        )
        print(
            "pdfplumber words = x_tolerance=2, y_tolerance=3, keep_blank_chars=True, return_chars=True:"
        )
        print(pdf_text)
        output_file = "../output/Pdfplumber.txt"
        with open(output_file, "a") as f:
            f.write(pdf_text)
    print(
        "End pdfplumber words = x_tolerance=2, y_tolerance=3, keep_blank_chars=True, return_chars=True"
    )
    print("")
    print("#-----------")
    print("")


"""
text_lines = page.extract_text_lines(layout=True, return_chars=False)
print("\n--- Extracted Text Lines ---")
for line in text_lines[:5]: # Print first 5 lines
print(line)
"""
