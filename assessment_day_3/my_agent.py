import json

from config import client, MODEL
from my_tools import TOOLS, TOOL_FUNCTIONS

SYSTEM_PROMPT = """
You are a Student Attendance Assistant.

Follow the ReAct approach:
1. Reason about what information is required.
2. Act by calling read_webpage or calculator when needed.
3. Observe the tool result.
4. Continue until you can give the final answer.

Use the attendance report for student attendance questions.
Use the calculator for arithmetic.
Do not invent attendance records.
If a file is missing, explain the error.
Only use the tools provided.
Keep the final answer clear and concise.
"""


def run_agent(question, max_steps=6):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question}
    ]

    print("\nQUESTION:", question)

    for step in range(max_steps):
        print(f"\n--- ReAct Step {step + 1} ---")

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            temperature=0,
            max_tokens=500
        )

        message = response.choices[0].message

        # No tool call: the model has produced a final answer.
        if not message.tool_calls:
            answer = message.content or "No answer returned."
            print("FINAL ANSWER:", answer)
            return answer

        assistant_message = {
            "role": "assistant",
            "content": message.content or "",
            "tool_calls": [
                {
                    "id": call.id,
                    "type": "function",
                    "function": {
                        "name": call.function.name,
                        "arguments": call.function.arguments
                    }
                }
                for call in message.tool_calls
            ]
        }

        messages.append(assistant_message)

        # Act: execute the tools requested by the model.
        for call in message.tool_calls:
            name = call.function.name
            raw_arguments = call.function.arguments

            print("ACTION:", name)
            print("ARGUMENTS:", raw_arguments)

            try:
                arguments = json.loads(raw_arguments)
                function = TOOL_FUNCTIONS.get(name)

                if function is None:
                    result = f"Error: Unknown tool '{name}'."
                else:
                    result = function(**arguments)

            except (json.JSONDecodeError, TypeError, KeyError) as error:
                result = f"Tool execution error: {error}"

            print("OBSERVATION:", str(result)[:1000])

            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": str(result)
            })

    print("STOPPED: Maximum ReAct steps reached.")
    return "Agent stopped because the step limit was reached."


if __name__ == "__main__":
    test_questions = [
        "Read data/attendance.html. Calculate Arun's attendance percentage and check whether he meets the 75% requirement.",
        "Read data/attendance.html. Calculate Priya's attendance percentage and check whether she meets the 75% requirement.",
        "What is 15% of 200?",
        "Read data/missing.html and tell me Arun's attendance."
    ]

    for question in test_questions:
        try:
            run_agent(question)
        except Exception as error:
            print("API or runtime error:", error)