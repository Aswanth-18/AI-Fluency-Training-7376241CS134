"""A small, grounded retrieval-augmented generation demonstration."""

from __future__ import annotations

from lc_config import get_llm, get_max_distance, get_vector_store


def main() -> None:
    vector_store = get_vector_store(require_existing=True)
    question = "What CGPA is required for the merit scholarship?"
    results = vector_store.similarity_search_with_score(question, k=4)
    relevant = [
        (document, distance)
        for document, distance in results
        if distance <= get_max_distance()
    ]
    if not relevant:
        print("I don't know based on the available documents.")
        return

    context = "\n\n".join(
        f"Source: {document.metadata.get('source', 'unknown')}\n"
        f"Passage: {document.page_content}"
        for document, _ in relevant
    )
    try:
        from langchain_core.prompts import ChatPromptTemplate
    except ImportError as error:
        raise RuntimeError(
            "langchain-core is missing. Run 'pip install -r requirements.txt'."
        ) from error

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Answer only using the supplied document passages. Cite the source "
                "filename in your answer. If the passages do not support an answer, "
                "reply exactly: I don't know based on the available documents.",
            ),
            ("human", "Question: {question}\n\nDocument passages:\n{context}"),
        ]
    )
    response = get_llm().invoke(
        prompt.format_messages(question=question, context=context)
    )
    print(f"Question: {question}")
    print(f"Answer: {response.content}")
    print("Retrieved sources: " + ", ".join(
        document.metadata.get("source", "unknown") for document, _ in relevant
    ))


if __name__ == "__main__":
    main()
