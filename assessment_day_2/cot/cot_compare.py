import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parents[1] / "agent")
)

from config import client, MODEL, banner


QUESTIONS = [
    (
        "A laptop costs Rs. 60,000. "
        "A 15% discount is applied and then a Rs. 1,000 "
        "delivery charge is added. What is the final price?"
    ),

    (
        "A warehouse has 25 boxes. Each box contains 12 products. "
        "If 80 products are sold, how many products remain?"
    ),

    (
        "Arun bought more products than Bala. "
        "Bala bought more products than Charlie. "
        "David bought fewer products than Charlie. "
        "Who bought the most and who bought the least?"
    )
]


DIRECT_PROMPT = """
You are a helpful assistant.
Give only the final answer.
Do not explain.
"""


COT_PROMPT = """
You are a helpful assistant.
Solve the problem step by step.
Number each step and show the calculation or reasoning.

After the steps, write the last line exactly as:

Final Answer: <answer>
"""


def ask(system_prompt, question):

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content.strip()


if __name__ == "__main__":

    banner("ASSESSMENT DAY 2 - DIRECT PROMPT VS CoT")

    for number, question in enumerate(QUESTIONS, start=1):

        print("\n" + "=" * 70)
        print(f"QUESTION {number}")
        print(question)

        print("\n--- WITHOUT CoT ---")
        print(ask(DIRECT_PROMPT, question))

        print("\n--- WITH CoT ---")
        print(ask(COT_PROMPT, question))