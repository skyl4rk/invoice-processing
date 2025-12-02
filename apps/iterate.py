# Import module
import os

# Assign directory
directory = r"../data/invoices_pdf"

# Iterate over files in directory
for name in os.listdir(directory):
    # Open file
    with open(os.path.join(directory, name)) as f:
        print(f"Filename: '{name}'")
        # Read content of file
        # pdf_file = f.read()

    print("------------")
