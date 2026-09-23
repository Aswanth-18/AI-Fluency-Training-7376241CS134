import sys
from pathlib import Path
from collections import Counter

# Get assessment_day_2 folder
BASE_DIR = Path(__file__).resolve().parents[1]

# Add agent and cot folders to Python path
sys.path.append(str(BASE_DIR / "agent"))
sys.path.append(str(BASE_DIR / "cot"))

# Reuse config.py from agent folder
from config import client, MODEL, banner

# Reuse questions and CoT prompt from cot folder
from cot_compare import QUESTIONS, COT_PROMPT


RUNS = 5
TEMPERATURE = 0.8


def ask(question):

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": COT_PROMPT
            },
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=TEMPERATURE
    )

    return response.choices[0].message.content.strip()


def final_answer(text):

    marker = "Final Answer:"

    if marker in text:
        return (
            text.split(marker, 1)[1]
            .strip()
            .splitlines()[0]
        )

    return text.splitlines()[-1].strip()


if __name__ == "__main__":

    banner("ASSESSMENT DAY 2 - SELF CONSISTENCY")

    question = QUESTIONS[0]

    print("\nQUESTION:")
    print(question)

    answers = []

    for i in range(1, RUNS + 1):

        response = ask(question)

        answer = final_answer(response)

        answers.append(answer)

        print("\n" + "-" * 60)
        print(f"RUN {i}")
        print("-" * 60)

        print(response)

    counts = Counter(answers)

    majority_answer, count = counts.most_common(1)[0]

    print("\n" + "=" * 70)
    print("SELF-CONSISTENCY RESULT")
    print("=" * 70)

    print(f"Answers observed: {answers}")
    print(f"Majority answer: {majority_answer}")
    print(f"Votes: {count}/{RUNS}")
    print(f"Temperature: {TEMPERATURE}")