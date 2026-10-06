# assessment_day_6/structured_outputs.py

import os
import json

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL = os.getenv("MODEL", "openai/gpt-oss-120b")


question = """
Extract the food order from this sentence:

I want 2 pizzas and 1 burger.

Return the item names and quantities.
"""


# ------------------------------------------------
# 1. No constraint
# ------------------------------------------------

print("=" * 60)
print("1. NO CONSTRAINT")
print("=" * 60)

response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "user", "content": question}
    ],
    temperature=0
)

raw = response.choices[0].message.content

print("Raw reply:")
print(raw)


# ------------------------------------------------
# 2. JSON MODE
# ------------------------------------------------

print("\n" + "=" * 60)
print("2. JSON MODE")
print("=" * 60)

response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {
            "role": "user",
            "content": question +
            "\nReturn only valid JSON."
        }
    ],
    response_format={"type": "json_object"},
    temperature=0
)

raw = response.choices[0].message.content

print("Raw reply:")
print(raw)

try:
    parsed = json.loads(raw)
    print("Parsed:")
    print(parsed)
except Exception as e:
    print("JSON error:", e)


# ------------------------------------------------
# 3. SCHEMA MODE
# ------------------------------------------------

print("\n" + "=" * 60)
print("3. SCHEMA MODE")
print("=" * 60)

schema = {
    "type": "object",
    "properties": {
        "orders": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "item": {"type": "string"},
                    "quantity": {"type": "integer"}
                },
                "required": ["item", "quantity"],
                "additionalProperties": False
            }
        }
    },
    "required": ["orders"],
    "additionalProperties": False
}

try:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": question}
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "food_order",
                "strict": True,
                "schema": schema
            }
        },
        temperature=0
    )

    raw = response.choices[0].message.content

    print("Raw reply:")
    print(raw)

    print("Parsed:")
    print(json.loads(raw))

except Exception as e:
    print("Schema mode error:", e)