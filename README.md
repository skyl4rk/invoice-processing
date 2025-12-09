The invoice processing agent takes a pdf invoice and shipping list, converts it into text format, checks to see if it is an invoice, shipping list or other filetype, requests that an LLM process the text to extract a structured JSON output which is then inserted in a database.

The working files are in the project directory. Example files are in the data directory. Sqlite3 databases are in the db directory.

The /project/main.py script processes the pdf file in the variable pdf_doc.

Batch process functions take all pdf files in a directory and processes them all in one process.

While this script works for the example invoices, each new type of invoice would need to be configured and checked. There are example processes for various python pdf to text packages which may help in determining the best method for converting pdf to text. 

Future development:

The database could be used to check whether the invoiced products agree with the shipped products. It can serve the basis of an inventory control system.  It could calculate the cost of materials for a given product.

To Do:

The delivery date response from the llm for shipping lists is unreliable, remove it from the database.

Upon completion of processing an invoice, move the invoice to a "processed" directory. 