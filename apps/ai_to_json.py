# import sqlite3
import os
from dotenv import load_dotenv

# from typing import List
# from pydantic import BaseModel, ValidationError
# import fitz  # PyMuPDF
from openai import OpenAI
import json
# import pandas as pd

# Load environment variables
load_dotenv()
api_key = os.getenv("API_KEY")
client = OpenAI(api_key=api_key)


def parse_invoice_with_ai(text: str) -> dict:
    """Use AI to extract structured invoice data as JSON."""
    prompt = f"""
    "Please extract the invoice number, invoice date, product number, description, quantity, unit price, and amount from: {text}"
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Cost-effective, or use "gpt-4o" for better accuracy
        messages=[
            {
                "role": "system",
                "content": "You are an expert invoice parser. Respond ONLY with valid JSON matching the exact schema above.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,  # Low temperature for consistent structured output
        response_format={"type": "json_object"},  # Enforce JSON output (OpenAI feature)
        max_tokens=100,
    )

    json_str = response.choices[0].message.content

    try:
        data = json.loads(json_str)
        print(data)
        return data
    except json.JSONDecodeError as e:
        raise ValueError(f"AI output is not valid JSON: {e}")


if __name__ == "__main__":
    # text_path = "../output/DoclingMarkdown.md"
    # text_path = "../output/DoclingStructure.json"
    # text_path = "../output/Fitz.txt"
    # text_path = "../output/Pdfplumber.txt"
    text_path = "../output/PyPDF2.txt"

    # output_file = "../data/json_results/DoclingMarkdown.json"
    # output_file = "../data/json_results/DoclingStructure.json"
    # output_file = "../data/json_results/Fitz.json"
    # output_file = "../data/json_results/Pdfplumber.json"
    output_file = "../data/json_results/PyPDF2.json"

    if not os.path.exists(text_path):
        print(f"❌ PDF not found: {text_path}")
        exit(1)

    try:
        json_result = parse_invoice_with_ai(text_path)

        # Save to file

        with open(output_file, "w") as f:
            f.write(str(json_result))

    except Exception as e:
        print(f"❌ Error: {e}")
