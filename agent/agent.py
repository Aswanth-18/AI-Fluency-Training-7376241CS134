import sys
import json

# Ensure UTF-8 output encoding for Windows terminal compatibility
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from config import client, MODEL, QUESTIONS, banner
from tools import TOOLS, TOOL_FUNCTIONS

SYSTEM_PROMPT = (
    "You are a college fee assistant. "
    "Never guess a fee. Always use get_course_fee for fee information. "
    "Use calculator for any arithmetic calculation. "
    "Available course codes are CS101, AI202, DS303. "
    "If no tool is needed, answer directly."
)

def clean_tool_name(name):
    """
    Fix malformed tool names that may be returned by some models.
    Example:
    calculator<|channel|>commentary
    becomes:
    calculator
    """
    if not name:
        return ""
    if "<|channel|>" in name:
        name = name.split("<|channel|>")[0]
    return name.strip()

def agent(question, max_steps=6, verbose=True):
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
        # -------------------------------------------------
        # 1. ASK LLM WHAT TO DO
        # -------------------------------------------------
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            temperature=0
        )

        message = response.choices[0].message

        # -------------------------------------------------
        # 2. NO TOOL -> FINAL ANSWER
        # -------------------------------------------------
        if not message.tool_calls:
            return (message.content or "").strip()

        # -------------------------------------------------
        # 3. STORE ASSISTANT TOOL CALL
        # -------------------------------------------------
        assistant_tool_calls = []
        for call in message.tool_calls:
            tool_name = clean_tool_name(call.function.name)
            assistant_tool_calls.append(
                {
                    "id": call.id,
                    "type": "function",
                    "function": {
                        "name": tool_name,
                        "arguments": call.function.arguments
                    }
                }
            )

        messages.append(
            {
                "role": "assistant",
                "content": message.content or "",
                "tool_calls": assistant_tool_calls
            }
        )

        # -------------------------------------------------
        # 4. EXECUTE TOOLS
        # -------------------------------------------------
        for call in message.tool_calls:
            name = clean_tool_name(call.function.name)

            # Parse arguments
            try:
                arguments = json.loads(call.function.arguments or "{}")
            except json.JSONDecodeError:
                arguments = {}

            # Find Python function
            function = TOOL_FUNCTIONS.get(name)

            if function is None:
                result = f"Unknown tool: {name}"
            else:
                try:
                    result = function(**arguments)
                except Exception as e:
                    result = f"Tool error: {e}"

            # Show execution
            if verbose:
                print(f"   step {step}: {name}({arguments}) -> {result}")

            # -------------------------------------------------
            # 5. SEND TOOL RESULT BACK TO LLM
            # -------------------------------------------------
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": str(result)
                }
            )

    # -------------------------------------------------
    # MAX STEPS REACHED
    # -------------------------------------------------
    return "Stopped: maximum steps reached without a final answer."

# =========================================================
# MAIN
# =========================================================
if __name__ == "__main__":
    banner("SYSTEM 3: AI AGENT")
    for question in QUESTIONS:
        print("Q:", question)
        answer = agent(question, max_steps=6, verbose=True)
        print("A:", answer)
        print("-" * 70)
