import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

BASE = "https://api.groq.com/openai/v1"
MODEL = os.getenv("MODEL", "openai/gpt-oss-120b")
API_KEY = os.getenv("GROQ_API_KEY")

PROMPTS = [
    "What does a shopping assistant do? Answer in one short sentence.",
    "A laptop costs Rs. 60,000. Give a 10% discount. What is the final price? Show only 2 short steps.",
    "Compare a laptop costing Rs. 60,000 and a monitor costing Rs. 15,000. Which is more expensive? Answer in one sentence."
]

SYSTEM_PROMPT = """
You are an E-Commerce Shopping Assistant.

Rules:
- Keep answers very short and clear.
- Help users compare products.
- Explain discounts briefly.
- Always show the calculation for price questions.
- Never invent product prices.
- Use Indian Rupees.
- Prefer 1 to 3 sentences.
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

    answer = response["choices"][0]["message"]["content"].strip()

    print("\nPrompt:", prompt)
    print(f"Time: {elapsed:.2f} seconds")
    print("Answer:", answer)


if __name__ == "__main__":

    print("=" * 70)
    print("SCENARIO 2 - E-COMMERCE SHOPPING ASSISTANT")
    print("=" * 70)

    for prompt in PROMPTS:
        run_groq(prompt)