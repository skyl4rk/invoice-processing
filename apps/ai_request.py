import requests
import json
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
client = OpenAI(api_key=api_key)

url = "https://openrouter.ai/api/v1/responses"
headers = {
    "Authorization": "Bearer YOUR_OPENROUTER_API_KEY",
    "Content-Type": "application/json",
}
data = {
    "model": "openai/o4-mini",
    "input": "What is the meaning of life?",
    "max_output_tokens": 9000,
}

response = requests.post(url, headers=headers, data=json.dumps(data))
print(response.json())
