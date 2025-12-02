from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")
client = OpenAI(api_key=api_key)


answer = client.responses.create(
    model="gpt-5.1",
    input="Who is the current president of France and how tall is he?",
    # tools=[{"type": "web_search_preview"}],
    tools=[{"type": "web_search"}],
    reasoning={"effort": "low"},
    instructions="Talk like a pirate.",
)

print(answer.output_text)
