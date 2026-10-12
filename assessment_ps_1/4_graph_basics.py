"""Show LangGraph state, nodes, edges, and conditional question routing."""

from __future__ import annotations

from typing import TypedDict


class HelpdeskState(TypedDict, total=False):
    question: str
    route: str
    reply: str


def main() -> None:
    try:
        from langgraph.graph import END, START, StateGraph
    except ImportError as error:
        raise RuntimeError(
            "langgraph is missing. Run 'pip install -r requirements.txt'."
        ) from error

    def classify(state: HelpdeskState) -> HelpdeskState:
        text = state["question"].lower()
        finance_terms = ("scholarship", "cgpa", "fee", "finance", "financial")
        route = "finance" if any(term in text for term in finance_terms) else (
            "hostel" if "hostel" in text or "warden" in text else "general"
        )
        return {"route": route}

    def student_finance(state: HelpdeskState) -> HelpdeskState:
        return {"reply": "Student finance desk: please consult the sample scholarship and fee policies."}

    def hostel_desk(state: HelpdeskState) -> HelpdeskState:
        return {"reply": "Hostel desk: the sample hostel rules are available in hostel_rules.md."}

    def general_helpdesk(state: HelpdeskState) -> HelpdeskState:
        return {"reply": "General helpdesk: please consult the relevant sample handbook document."}

    graph_builder = StateGraph(HelpdeskState)
    graph_builder.add_node("classify", classify)
    graph_builder.add_node("student_finance", student_finance)
    graph_builder.add_node("hostel_desk", hostel_desk)
    graph_builder.add_node("general_helpdesk", general_helpdesk)
    graph_builder.add_edge(START, "classify")
    graph_builder.add_conditional_edges(
        "classify",
        lambda state: state["route"],
        {
            "finance": "student_finance",
            "hostel": "hostel_desk",
            "general": "general_helpdesk",
        },
    )
    graph_builder.add_edge("student_finance", END)
    graph_builder.add_edge("hostel_desk", END)
    graph_builder.add_edge("general_helpdesk", END)
    graph = graph_builder.compile()

    questions = [
        "What CGPA is required for a scholarship?",
        "What time should I return to the hostel?",
        "Where can I ask about library timings?",
    ]
    for question in questions:
        result = graph.invoke({"question": question})
        print(f"Question: {question}")
        print(f"Route: {result['route']}")
        print(f"Reply: {result['reply']}\n")


if __name__ == "__main__":
    main()
