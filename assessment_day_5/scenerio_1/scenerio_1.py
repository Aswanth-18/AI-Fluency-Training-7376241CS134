import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

BASE = "https://api.groq.com/openai/v1"
MODEL = os.getenv("MODEL", "openai/gpt-oss-120b")
API_KEY = os.getenv("GROQ_API_KEY")

PROMPTS = [
    "What is a college fee assistant?",
    "A course costs Rs. 18,000 with a 15% scholarship. What is payable? Show the steps.",
    "Explain the fee calculation in a simple way for a student."
]

SYSTEM_PROMPT = """
You are a College Fee Assistant.

Rules:
- Be clear and concise.
- Always show calculations for fee-related questions.
- Use Indian Rupees.
- Never invent a fee that is not provided.
- Use a friendly student-oriented tone.
"""

def run_groq(prompt):
    start = time.time()

    response = requests.post(
        f"{BASE}/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": MODEL,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0
        },
        timeout=60
    ).json()

    elapsed = time.time() - start

    if "choices" not in response:
        print("Error:", response)
        return

    answer = response["choices"][0]["message"]["content"]

    print("\nPrompt:", prompt)
    print(f"Time: {elapsed:.2f} seconds")
    print("Answer:", answer)


if __name__ == "__main__":

    print("=" * 70)
    print("SCENARIO 1 - COLLEGE FEE ASSISTANT")
    print("=" * 70)

    for prompt in PROMPTS:
        run_groq(prompt)