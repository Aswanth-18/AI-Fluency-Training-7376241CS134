import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

BASE = "https://api.groq.com/openai/v1"
MODEL = os.getenv("MODEL", "openai/gpt-oss-120b")
API_KEY = os.getenv("GROQ_API_KEY")

PROMPTS = [
    "What is an AI agent? Answer in one short sentence.",
    "What is a stack in data structures? Explain in two short sentences.",
    "What is the difference between AI and machine learning? Answer briefly."
]

SYSTEM_PROMPT = """
You are a College Study Assistant.

Rules:
- Explain technical concepts in simple language.
- Keep answers short and clear.
- Use small examples when useful.
- Prefer 1 to 3 sentences.
- Avoid unnecessary complexity.
- Be student-friendly.
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
    print("SCENARIO 3 - COLLEGE STUDY ASSISTANT")
    print("=" * 70)

    for prompt in PROMPTS:
        run_groq(prompt)