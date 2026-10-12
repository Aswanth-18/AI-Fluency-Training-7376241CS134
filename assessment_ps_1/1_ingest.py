"""Load handbook Markdown files, split them, and replace the Chroma contents."""

from __future__ import annotations

import hashlib

from lc_config import CHROMA_DIR, DATA_DIR, get_vector_store


def main() -> None:
    try:
        from langchain_community.document_loaders import TextLoader
        from langchain_text_splitters import RecursiveCharacterTextSplitter
    except ImportError as error:
        raise RuntimeError(
            "Document ingestion dependencies are missing. Run "
            "'pip install -r requirements.txt' in the activated virtual environment."
        ) from error

    files = sorted(DATA_DIR.glob("*.md"))
    if not files:
        raise FileNotFoundError(
            f"No Markdown handbook files found in {DATA_DIR}. Add the sample data "
            "documents before running ingestion."
        )

    documents = []
    for path in files:
        loaded = TextLoader(str(path), encoding="utf-8").load()
        for document in loaded:
            document.metadata["source"] = path.name
        documents.extend(loaded)

    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
    chunks = splitter.split_documents(documents)
    if not chunks:
        raise RuntimeError("The handbook files contained no text to index.")

    vector_store = get_vector_store()

    # Replace the collection contents so repeated runs cannot leave stale chunks.
    existing_ids = vector_store.get()["ids"]
    for offset in range(0, len(existing_ids), 500):
        vector_store.delete(ids=existing_ids[offset : offset + 500])

    ids = []
    for index, chunk in enumerate(chunks):
        source = chunk.metadata.get("source", "unknown")
        digest = hashlib.sha256(chunk.page_content.encode("utf-8")).hexdigest()[:16]
        ids.append(f"{source}:{index}:{digest}")
    vector_store.add_documents(documents=chunks, ids=ids)

    stored_count = len(vector_store.get()["ids"])
    print(f"Source documents loaded: {len(files)}")
    print(f"Text chunks created: {len(chunks)}")
    print(f"Vectors stored: {stored_count}")
    print(f"Chroma directory: {CHROMA_DIR}")


if __name__ == "__main__":
    main()
