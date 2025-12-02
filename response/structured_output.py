from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)


response = client.responses.create(
    model="tngtech/deepseek-r1t2-chimera:free",
    input="Jane, 54 years old",
    text={
        "format": {
            "type": "json_schema",
            "name": "person",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "minLength": 1},
                    "age": {"type": "number", "minimum": 0, "maximum": 130},
                },
                "required": ["name", "age"],
                "additionalProperties": False,
            },
        }
    },
)

print(response.output_text)
