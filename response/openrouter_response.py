from openai import OpenAI

# import requests
# import json
import os
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

response = client.responses.create(
    model="tngtech/deepseek-r1t2-chimera:free",
    input="How many bears per sqare mile are there in the upper peninsuala of Michigan?",
)

print(response.output_text)
