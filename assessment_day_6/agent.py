# assessment_day_6/agent.py

import os
import json
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from tools import TOOLS, TOOL_FUNCTIONS
from validator import validate_arguments


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("MODEL", "openai/gpt-oss-120b")

if not API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file.")


client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=API_KEY
)


# ============================================================
# SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are a food ordering assistant.

You can use tools to:
1. Check the price of a food item.
2. Calculate the total cost of an order.

Available food items:
- burger
- pizza
- sandwich

Use the tools whenever the user asks for a price or calculation.

Keep the final answer short and clear.
"""


# ============================================================
# MAIN AGENT
# ============================================================

def run_agent(user_question, max_steps=5):

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": user_question
        }
    ]

    # Used to detect repeated identical calls
    previous_calls = set()

    for step in range(1, max_steps + 1):

        print(f"\n--- Step {step} ---")

        # ----------------------------------------------------
        # CALL MODEL
        # ----------------------------------------------------

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            temperature=0,
            max_tokens=300
        )

        choice = response.choices[0]
        message = choice.message
        finish_reason = choice.finish_reason

        print("finish_reason:", finish_reason)

        # ----------------------------------------------------
        # RETRY IF OUTPUT WAS TRUNCATED
        # ----------------------------------------------------

        if finish_reason == "length":

            print("Output was truncated.")
            print("Retrying with larger max_tokens...")

            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=TOOLS,
                tool_choice="auto",
                temperature=0,
                max_tokens=600
            )

            choice = response.choices[0]
            message = choice.message
            finish_reason = choice.finish_reason

            print("Retry finish_reason:", finish_reason)

        # ----------------------------------------------------
        # NO TOOL CALL
        # ----------------------------------------------------

        if not message.tool_calls:

            print("\nFinal answer:")
            print(message.content)

            return message.content

        # ----------------------------------------------------
        # ADD ASSISTANT TOOL MESSAGE
        #
        # IMPORTANT:
        # Do NOT use message.model_dump()
        # because Groq may reject unsupported fields
        # such as "annotations".
        # ----------------------------------------------------

        assistant_message = {
            "role": "assistant",
            "content": message.content,
            "tool_calls": []
        }

        for call in message.tool_calls:

            assistant_message["tool_calls"].append({
                "id": call.id,
                "type": "function",
                "function": {
                    "name": call.function.name,
                    "arguments": call.function.arguments
                }
            })

        messages.append(assistant_message)

        # ----------------------------------------------------
        # HANDLE ALL TOOL CALLS
        # ----------------------------------------------------

        for tool_call in message.tool_calls:

            tool_name = tool_call.function.name
            raw_arguments = tool_call.function.arguments

            print("\nTool call:")
            print("Tool:", tool_name)
            print("Arguments:", raw_arguments)

            # =================================================
            # STAGE 1 - PARSE JSON
            # =================================================

            try:

                args = json.loads(raw_arguments)

            except json.JSONDecodeError:

                result = (
                    "Invalid JSON arguments. "
                    "Please provide valid JSON arguments."
                )

                print("Validation:", result)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })

                continue

            # =================================================
            # REPEATED IDENTICAL CALL CHECK
            # =================================================

            call_signature = (
                tool_name + "|" +
                json.dumps(args, sort_keys=True)
            )

            if call_signature in previous_calls:

                result = (
                    "Repeated identical tool call detected. "
                    "Please use a different action."
                )

                print("Guard:", result)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })

                continue

            previous_calls.add(call_signature)

            # =================================================
            # STAGE 2 - LOOK UP TOOL
            # =================================================

            if tool_name not in TOOL_FUNCTIONS:

                result = (
                    f"Unknown tool '{tool_name}'. "
                    "Use one of the available tools."
                )

                print("Tool lookup:", result)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })

                continue

            # =================================================
            # STAGE 3 - VALIDATE ARGUMENTS
            # =================================================

            validation_error = validate_arguments(
                tool_name,
                args
            )

            if validation_error:

                print("Validation:", validation_error)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": validation_error
                })

                continue

            # =================================================
            # STAGE 4 - EXECUTE TOOL
            # =================================================

            try:

                function = TOOL_FUNCTIONS[tool_name]

                result = function(**args)

                print("Tool result:", result)

            except Exception as e:

                result = f"Tool execution error: {str(e)}"

                print("Execution error:", result)

            # =================================================
            # RETURN TOOL RESULT TO MODEL
            # =================================================

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result)
            })

    # ========================================================
    # MAXIMUM STEPS REACHED
    # ========================================================

    result = "Maximum number of agent steps reached."

    print("\n", result)

    return result


# ============================================================
# TEST QUESTIONS
# ============================================================

if __name__ == "__main__":

    questions = [

        # 1. Single tool
        "What is the price of a burger?",

        # 2. Single calculation
        "Calculate the cost of 2 pizzas.",

        # 3. Two tools
        "What is the price of a burger and calculate the cost of 2 pizzas?",

        # 4. Invalid-value temptation
        "What is the price of icecream?",

        # 5. No tool
        "Hello, how are you?"
    ]

    for question in questions:

        print("\n")
        print("=" * 70)
        print("QUESTION:", question)
        print("=" * 70)

        try:
            run_agent(question)

        except Exception as e:

            print("\nAgent error:")
            print(e)