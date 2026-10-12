import json

from config import client, MODEL
from my_tools import TOOLS, TOOL_FUNCTIONS

MAX_STEPS = 8
MAX_TOOL_OUTPUT = 1200
MAX_CONTEXT_CHARS = 14000

SYSTEM_PROMPT = """
You are a Student Attendance Assistant.

Use the ReAct cycle:
1. Reason about the question.
2. Act by calling a suitable tool.
3. Observe the result.
4. Give the final answer when enough information is available.

Use read_webpage to inspect the attendance report.
Use calculator for arithmetic.
Never invent student records.
If a tool returns an error, explain it honestly.
Use only the available tools.
Do not repeat an identical tool call.
Keep the final answer concise.
"""


def context_size(messages):
    """Estimate context usage by counting message characters."""
    return sum(
        len(str(message.get("content", "")))
        + len(str(message.get("tool_calls", "")))
        for message in messages
    )


def run_agent_fixed(question):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question}
    ]

    # Stores the name and arguments of previous tool calls.
    seen_calls = set()

    print("\nQUESTION:", question)

    for step in range(MAX_STEPS):
        # Context-budget guard.
        size = context_size(messages)

        if size > MAX_CONTEXT_CHARS:
            print("CONTEXT GUARD: Conversation budget exceeded.")
            return (
                "Stopped safely because the conversation exceeded "
                "the configured context budget."
            )

        print(f"\n--- ReAct Step {step + 1} ---")
        print("Estimated context characters:", size)

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            temperature=0,
            max_tokens=400
        )

        message = response.choices[0].message

        if not message.tool_calls:
            answer = message.content or "No answer returned."
            print("FINAL ANSWER:", answer)
            return answer

        messages.append({
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
        })

        for call in message.tool_calls:
            name = call.function.name
            raw_arguments = call.function.arguments

            print("ACTION:", name)
            print("ARGUMENTS:", raw_arguments)

            # Repeat detection.
            signature = (name, raw_arguments)

            if signature in seen_calls:
                result = (
                    f"Error: Repeated tool call detected for '{name}'. "
                    "Try a different action or provide a final answer."
                )
                print("REPEAT GUARD:", result)

            else:
                seen_calls.add(signature)

                try:
                    arguments = json.loads(raw_arguments)
                    function = TOOL_FUNCTIONS.get(name)

                    if function is None:
                        result = f"Error: Unknown tool '{name}'."

                    elif not isinstance(arguments, dict):
                        result = "Error: Tool arguments must be a JSON object."

                    else:
                        result = function(**arguments)

                except (json.JSONDecodeError, TypeError, KeyError) as error:
                    result = f"Tool execution error: {error}"

            # Truncate large tool output before adding it to the context.
            result = str(result)

            if len(result) > MAX_TOOL_OUTPUT:
                result = (
                    result[:MAX_TOOL_OUTPUT]
                    + "\n[Tool output truncated]"
                )
                print("OUTPUT GUARD: Tool result truncated.")

            print("OBSERVATION:", result[:300])

            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": result
            })

        # Recheck the context after tool results are added.
        if context_size(messages) > MAX_CONTEXT_CHARS:
            print("CONTEXT GUARD: Tool results exceeded the budget.")
            return (
                "Stopped safely after tool execution because "
                "the conversation exceeded the configured budget."
            )

    print("STEP GUARD: Maximum ReAct steps reached.")
    return "Agent stopped safely after reaching the maximum step count."


if __name__ == "__main__":
    test_questions = [
        "Read data/attendance.html and calculate Arun's attendance percentage.",
        "Read data/attendance.html and check whether Priya meets the 75% requirement.",
        "What is 15% of 200?",
        "Read data/missing.html and tell me the attendance percentage."
        "Read data/large_attendance.html and summarize the attendance report."
    ]

    for question in test_questions:
        try:
            run_agent_fixed(question)
        except Exception as error:
            print("API or runtime error:", error)