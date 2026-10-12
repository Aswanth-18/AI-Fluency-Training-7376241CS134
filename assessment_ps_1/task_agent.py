"""Four-tool scholarship helpdesk assessment using LangGraph and Chroma."""

from __future__ import annotations

import ast
import operator
from collections.abc import Callable
from typing import Any

from lc_config import get_max_distance, get_vector_store

COURSE_FEES = {
    "CS101": 12_000,
    "AI202": 18_000,
    "DS303": 15_000,
}
THREAD_ID = "scholarship-helpdesk-assessment"
MAX_RECURSION = 12
ASSESSMENT_QUESTIONS = [
    "What CGPA do I need for the merit scholarship?",
    "My CGPA is 9.4. Can I apply for the scholarship?",
    "What is the total fee for CS101 and AI202, plus the maximum late fee?",
    "And if I pay only 5 days late instead?",
    "What is the capital of France?",
]


def _calculator_value(node: ast.AST) -> int | float:
    binary_operators: dict[type[ast.operator], Callable[[Any, Any], Any]] = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
    }
    unary_operators: dict[type[ast.unaryop], Callable[[Any], Any]] = {
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
    }

    if isinstance(node, ast.Expression):
        return _calculator_value(node.body)
    if isinstance(node, ast.Constant) and type(node.value) in (int, float):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in binary_operators:
        left = _calculator_value(node.left)
        right = _calculator_value(node.right)
        if isinstance(node.op, ast.Div) and right == 0:
            raise ZeroDivisionError("division by zero")
        return binary_operators[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and type(node.op) in unary_operators:
        return unary_operators[type(node.op)](_calculator_value(node.operand))
    raise ValueError("Only numeric constants and +, -, *, /, and parentheses are allowed.")


def build_tools():
    try:
        from langchain_core.tools import tool
    except ImportError as error:
        raise RuntimeError(
            "langchain-core is missing. Run 'pip install -r requirements.txt'."
        ) from error

    @tool
    def search_handbook(query: str) -> str:
        """Search sample college handbook policies and cite source filenames."""
        vector_store = get_vector_store(require_existing=True)
        results = vector_store.similarity_search_with_score(query, k=4)
        threshold = get_max_distance()
        print(f"  search_handbook query: {query}")
        for document, distance in results:
            print(
                "    candidate "
                f"distance={distance:.4f}, "
                f"source={document.metadata.get('source', 'unknown')}"
            )
        relevant = [
            (document, distance)
            for document, distance in results
            if distance <= threshold
        ]
        if not relevant:
            return (
                "NO_MATCH: No retrieved passage passed the configured relevance "
                f"threshold (MAX_DISTANCE={threshold:.4f}). The question is not "
                "covered in the available sample college documents."
            )
        return "\n\n".join(
            f"Source: {document.metadata.get('source', 'unknown')}\n"
            f"Distance: {distance:.4f}\nPassage: {document.page_content}"
            for document, distance in relevant
        )

    @tool
    def get_course_fee(course_code: str) -> str:
        """Look up the sample fee for a course code such as CS101."""
        normalized = course_code.strip().upper()
        fee = COURSE_FEES.get(normalized)
        if fee is None:
            return (
                f"Unknown course code {course_code!r}. Available sample course "
                f"codes: {', '.join(COURSE_FEES)}."
            )
        return f"Sample fee for {normalized}: Rs. {fee:,}."

    @tool
    def calculator(expression: str) -> str:
        """Safely calculate an expression using +, -, *, /, and parentheses."""
        try:
            parsed = ast.parse(expression, mode="eval")
            result = _calculator_value(parsed)
        except ZeroDivisionError:
            return "Calculation error: division by zero is not allowed."
        except (SyntaxError, ValueError, TypeError, OverflowError) as error:
            return f"Calculation error: invalid expression ({error})."
        return f"{expression} = {result:g}"

    @tool
    def check_scholarship_eligibility(cgpa: float) -> str:
        """Check the sample merit scholarship CGPA threshold."""
        if not 0 <= cgpa <= 10:
            return "Invalid CGPA: enter a value from 0 to 10."
        if cgpa >= 9.0:
            return (
                f"CGPA {cgpa:g} meets the sample merit scholarship CGPA threshold "
                "(9.0 or above), so the student is eligible to apply based on CGPA. "
                "No standing arrears and the application deadline before 31 August "
                "are separate requirements; arrears status has not been verified."
            )
        return (
            f"CGPA {cgpa:g} is below the sample merit scholarship CGPA threshold "
            "(9.0), so the student is not eligible based on CGPA. No standing "
            "arrears and the application deadline before 31 August are separate "
            "requirements; arrears status has not been verified."
        )

    return [
        search_handbook,
        get_course_fee,
        calculator,
        check_scholarship_eligibility,
    ]


def _format_answer(content: Any) -> str:
    if isinstance(content, str):
        return content
    return str(content)


def main() -> None:
    try:
        from langchain_core.messages import HumanMessage
        from langgraph.checkpoint.memory import InMemorySaver
        from langgraph.graph import END, START, MessagesState, StateGraph
        from langgraph.prebuilt import ToolNode, tools_condition
    except ImportError as error:
        raise RuntimeError(
            "LangChain/LangGraph dependencies are missing. Run "
            "'pip install -r requirements.txt'."
        ) from error

    from lc_config import get_llm

    tools = build_tools()
    tool_names = {item.name for item in tools}
    model = get_llm().bind_tools(tools)
    system_prompt = (
        "You are a careful student scholarship and financial-support helpdesk. "
        "Use the tools for every relevant fact; never invent policies or answer "
        "outside the sample documents. For scholarship-policy questions, call "
        "search_handbook. For an individual CGPA eligibility question, call "
        "check_scholarship_eligibility. For course prices, call get_course_fee "
        "for each course. For policy late-fee facts, call search_handbook. "
        "For a total, use calculator after you have retrieved the component "
        "values. For follow-ups, use the full conversation history to resolve "
        "what 'instead' refers to and call whatever tools are needed for the "
        "updated calculation. In particular, five late days use the published "
        "daily late-fee amount, not the maximum cap. If search_handbook returns "
        "NO_MATCH, state that the question is not covered in the available "
        "college documents and do not answer from general knowledge. For every "
        "other factual question, including seemingly general-knowledge "
        "questions, call search_handbook to establish whether it is covered. "
        "Name handbook source files when reporting policy. All data are sample "
        "policies, not verified rules for a real institution."
    )

    def agent(state: MessagesState) -> dict[str, list[Any]]:
        from langchain_core.messages import SystemMessage

        response = model.invoke(
            [SystemMessage(content=system_prompt), *state["messages"]]
        )
        return {"messages": [response]}

    builder = StateGraph(MessagesState)
    builder.add_node("agent", agent)
    builder.add_node("tools", ToolNode(tools))
    builder.add_edge(START, "agent")
    builder.add_conditional_edges("agent", tools_condition)
    builder.add_edge("tools", "agent")
    graph = builder.compile(checkpointer=InMemorySaver())
    config = {
        "configurable": {"thread_id": THREAD_ID},
        "recursion_limit": MAX_RECURSION,
    }

    for number, question in enumerate(ASSESSMENT_QUESTIONS, start=1):
        print(f"\n{'=' * 72}")
        print(f"Question {number}: {question}")
        result = graph.invoke({"messages": [HumanMessage(content=question)]}, config)
        messages = result["messages"]
        # The checkpoint retains earlier turns; identify this turn by walking
        # backward to the latest user message.
        latest_user_index = max(
            index
            for index, message in enumerate(messages)
            if getattr(message, "type", "") == "human"
        )
        turn_messages = messages[latest_user_index + 1 :]
        calls = [
            (call["name"], call["args"])
            for message in turn_messages
            for call in getattr(message, "tool_calls", [])
        ]
        called_names = [name for name, _ in calls]
        if calls:
            for name, arguments in calls:
                print(f"Tool call: {name}({arguments})")
        else:
            print("Tool calls: none")
        unknown_names = set(called_names) - tool_names
        if unknown_names:
            raise RuntimeError(f"Unexpected tool call(s): {sorted(unknown_names)}")
        final_message = next(
            (
                message
                for message in reversed(turn_messages)
                if getattr(message, "type", "") == "ai"
                and not getattr(message, "tool_calls", [])
            ),
            None,
        )
        if final_message is None:
            raise RuntimeError(
                "The agent did not produce a final response. Check model tool "
                "calling support and the recursion limit."
            )
        answer = _format_answer(final_message.content)
        no_match = any(
            getattr(message, "type", "") == "tool"
            and getattr(message, "name", "") == "search_handbook"
            and isinstance(getattr(message, "content", None), str)
            and message.content.startswith("NO_MATCH:")
            for message in turn_messages
        )
        if no_match:
            answer = (
                "That question is not covered in the available college documents."
            )
        print(f"Final response: {answer}")


if __name__ == "__main__":
    main()
