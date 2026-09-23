import json

from config import client, MODEL
from tools import TOOLS, TOOL_FUNCTIONS


SYSTEM_PROMPT = """
You are an e-commerce shopping assistant.

You have access to two tools:

1. get_product_price
2. calculator

Rules:

- Never guess product prices.
- Always use get_product_price when you need a product price.
- Always use calculator for arithmetic.
- Think about what information is needed before answering.
- Use tools when required.
- After getting enough information, provide a clear final answer.
"""


def clean_tool_name(name):
    if not name:
        return ""

    if "<|channel|>" in name:
        name = name.split("<|channel|>")[0]

    return name.strip()


def agent(question, max_steps=8):

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": question
        }
    ]

    for step in range(1, max_steps + 1):

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            temperature=0
        )

        message = response.choices[0].message

        # No tool call → final answer
        if not message.tool_calls:

            print(f"\n[Step {step}] FINAL RESPONSE")
            print(message.content)

            return message.content

        # Add assistant tool-call message
        messages.append(message)

        print(f"\n[Step {step}] THOUGHT / ACTION")

        for tool_call in message.tool_calls:

            tool_name = clean_tool_name(
                tool_call.function.name
            )

            arguments = json.loads(
                tool_call.function.arguments
            )

            print(f"Action: {tool_name}")
            print(f"Arguments: {arguments}")

            if tool_name not in TOOL_FUNCTIONS:

                result = "Unknown tool"

            else:

                result = TOOL_FUNCTIONS[tool_name](
                    **arguments
                )

            print(f"Observation: {result}")

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_name,
                    "content": str(result)
                }
            )

    return "Maximum number of steps reached."