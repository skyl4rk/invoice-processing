import fitz


# pdf_path = "../data/invoices_pdf/202501-invoice.pdf"

pdf_path = "../data/shipping_lists_pdf/2501-shipping-list.pdf"

print("")
print("#-----------")
print("Begin fitz default:")
file = fitz.open(pdf_path)
for page in file:
    text2 = page.get_text()
print(text2)
# Save to file
output_file = "../output/Fitz.txt"
with open(output_file, "w") as f:
    f.write(text2)
print("End fitz default.")
print("")
print("#----------------")

print("Begin fitz text:")
file = fitz.open(pdf_path)
for page in file:
    text2 = page.get_text("text")
print(text2)
# Save to file
output_file = "../output/Fitz.txt"
with open(output_file, "a") as f:
    f.write(text2)
print("End fitz text.")
print("")
print("#----------------")


print("Begin fitz text, flags=fitz.TEXT_PRESERVE_WHITESPACE:")
file = fitz.open(pdf_path)
for page in file:
    text2 = page.get_text("text", flags=fitz.TEXT_PRESERVE_WHITESPACE)
print(text2)
# Save to file
output_file = "../output/Fitz.txt"
with open(output_file, "a") as f:
    f.write(text2)

print("End fitz text, flags=fitz.TEXT_PRESERVE_WHITESPACE.")
print("")
print("#----------------")

"""
print("Begin fitz blocks:")
file = fitz.open(pdf_path)
for page in file:
    text2 = page.get_text("blocks")
for item in text2:
    print(item)
    print("\n")
output_file = "../output/Fitz.txt"
with open(output_file, "a") as f:
    for item in text2:
        f.write(item)
        f.write("\n")
print("End fitz blocks.")
print("")
print("#----------------")


print("Begin fitz words:")
file = fitz.open(pdf_path)
for page in file:
    text2 = page.get_text("words")
print(text2)
output_file = "../output/Fitz.txt"
with open(output_file, "a") as f:
    f.write(text2)
print("End fitz words.")
print("")
print("#----------------")
"""

print("Begin fitz html:")
file = fitz.open(pdf_path)
for page in file:
    text2 = page.get_text("html")
print(text2)
output_file = "../output/Fitz.txt"
with open(output_file, "a") as f:
    f.write(text2)
print("End fitz html.")
print("")
print("#----------------")

"""
print("Begin fitz dict:")
file = fitz.open(pdf_path)
for page in file:
    text2 = page.get_text("dict")
print(text2)
output_file = "../output/Fitz.txt"
with open(output_file, "a") as f:
    f.write(text2)
print("End fitz dict.")
print("")
print("#----------------")


print("Begin fitz json:")
file = fitz.open(pdf_path)
for page in file:
    text2 = page.get_text("json")
print(text2)
output_file = "../output/Fitz.txt"
with open(output_file, "a") as f:
    f.write(text2)
print("End fitz json.")
print("")
print("#----------------")


print("Begin fitz rawdict:")
file = fitz.open(pdf_path)
for page in file:
    text2 = page.get_text("rawdict")
print(text2)
output_file = "../output/Fitz.txt"
with open(output_file, "a") as f:
    f.write(text2)
print("End fitz rawdict.")
print("")
print("#----------------")


print("Begin fitz rawjson:")
file = fitz.open(pdf_path)
for page in file:
    text2 = page.get_text("rawjson")
print(text2)
output_file = "../output/Fitz.txt"
with open(output_file, "a") as f:
    f.write(text2)
print("End fitz rawjson.")
print("")
print("#----------------")
"""
