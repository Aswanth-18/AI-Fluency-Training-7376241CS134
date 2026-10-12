"""Run sample handbook searches and display Chroma cosine distances."""

from __future__ import annotations

from lc_config import get_vector_store

QUERIES = [
    "What CGPA is required for the merit scholarship?",
    "What is the late fee?",
    "What are the library timings?",
    "What is the capital of France?",
]


def main() -> None:
    vector_store = get_vector_store(require_existing=True)
    for query in QUERIES:
        print(f"\nQuery: {query}")
        results = vector_store.similarity_search_with_score(query, k=3)
        if not results:
            print("  No matching passages found.")
            continue
        for document, distance in results:
            source = document.metadata.get("source", "unknown")
            passage = " ".join(document.page_content.split())
            if len(passage) > 220:
                passage = passage[:217] + "..."
            print(f"  Distance: {distance:.4f}")
            print(f"  Source: {source}")
            print(f"  Passage: {passage}")


if __name__ == "__main__":
    main()
