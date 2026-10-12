"""A minimal tool-using LangGraph handbook agent with in-memory memory."""

from __future__ import annotations


def main() -> None:
    try:
        from langchain_core.messages import HumanMessage, SystemMessage
        from langchain_core.tools import tool
        from langgraph.checkpoint.memory import InMemorySaver
        from langgraph.graph import END, START, MessagesState, StateGraph
        from langgraph.prebuilt import ToolNode, tools_condition
    except ImportError as error:
        raise RuntimeError(
            "LangChain/LangGraph dependencies are missing. Run "
            "'pip install -r requirements.txt'."
        ) from error

    from lc_config import get_llm, get_max_distance, get_vector_store

    vector_store = get_vector_store(require_existing=True)

    @tool
    def search_handbook(query: str) -> str:
        """Search the sample handbook and return relevant passages with filenames."""
        results = vector_store.similarity_search_with_score(query, k=4)
        matching = [
            (document, distance)
            for document, distance in results
            if distance <= get_max_distance()
        ]
        if not matching:
            return "NO_MATCH: The question is not covered in the available documents."
        return "\n\n".join(
            f"Source: {document.metadata.get('source', 'unknown')}\n"
            f"Distance: {distance:.4f}\nPassage: {document.page_content}"
            for document, distance in matching
        )

    tools = [search_handbook]
    model = get_llm().bind_tools(tools)

    def agent(state: MessagesState):
        system_message = SystemMessage(
            content=(
                "You are a student handbook helpdesk. For policy questions, call "
                "search_handbook before answering. Base the answer only on returned "
                "passages and name their source files. If the tool returns NO_MATCH, "
                "do not answer from general knowledge; say the question is not "
                "covered in the available college documents. Use conversation "
                "history to resolve follow-up questions. Do not invent policy."
            )
        )
        return {"messages": [model.invoke([system_message, *state["messages"]])]}

    builder = StateGraph(MessagesState)
    builder.add_node("agent", agent)
    builder.add_node("tools", ToolNode(tools))
    builder.add_edge(START, "agent")
    builder.add_conditional_edges("agent", tools_condition)
    builder.add_edge("tools", "agent")
    graph = builder.compile(checkpointer=InMemorySaver())

    result = graph.invoke(
        {"messages": [HumanMessage(content="What CGPA is required for the merit scholarship?")]},
        {
            "configurable": {"thread_id": "agentic-rag-demo"},
            "recursion_limit": 8,
        },
    )
    for message in result["messages"]:
        if getattr(message, "tool_calls", None):
            for call in message.tool_calls:
                print(f"Tool call: {call['name']}({call['args']})")
    print(f"Final response: {result['messages'][-1].content}")


if __name__ == "__main__":
    main()
