from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")
client = OpenAI(api_key=api_key)


response = client.responses.create(
    model="gpt-5-nano",
    input="What is the best beach on Lake Michigan in Michigan?",
    max_output_tokens=9000,
)

print(response.output_text)
