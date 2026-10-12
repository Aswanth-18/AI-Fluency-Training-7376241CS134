# Assessment Results and Analysis

## Project objective

Build a sample student scholarship and financial-support helpdesk that combines
retrieval-augmented generation (RAG), a Chroma vector store, and a LangGraph
tool-using agent.

## Scenario

The application answers questions against explicitly illustrative sample
college documents. These documents are not real institutional rules. Course
fees are separately provided as sample tool data.

## Architecture and tools

1. `1_ingest.py` loads Markdown documents, attaches their filenames as source
   metadata, splits them into 300-character chunks with 50-character overlap,
   and replaces the persistent Chroma collection.
2. `2_search.py` runs similarity searches and reports cosine distances, source
   filenames, and passages.
3. `3_rag_chain.py` generates an answer only when retrieved evidence passes the
   configured distance threshold.
4. `4_graph_basics.py` demonstrates LangGraph state, nodes, edges, and conditional
   routing.
5. `5_agentic_rag.py` demonstrates a tool-calling graph with an in-memory
   checkpointer.
6. `task_agent.py` exposes `search_handbook`, `get_course_fee`, `calculator`,
   and `check_scholarship_eligibility` to a checkpointed LangGraph agent.

## Ingestion

Not run in the inspected environment: its project virtual environment does not
currently contain the LangChain, LangGraph, Chroma, or FastEmbed packages.

| Measure | Actual result |
|---|---|
| Markdown documents loaded | Pending ingestion |
| Chunks created | Pending ingestion |
| Vectors stored | Pending ingestion |

After installing dependencies and configuring an embedding model, run
`python 1_ingest.py` and copy its printed counts here.

## Search results

Not run: the Chroma database does not exist until ingestion completes. Run
`python 2_search.py` and copy the distances and source results here.

## Five-question assessment

No model runs were performed, so actual calls, responses, and correctness are
intentionally not represented as test results.

| # | Question | Actual tools called | Actual answer | Correctness | Observations |
|---|---|---|---|---|---|
| 1 | What CGPA do I need for the merit scholarship? | Not run | Not run | Not assessed | Run `python task_agent.py` after setup. |
| 2 | My CGPA is 9.4. Can I apply for the scholarship? | Not run | Not run | Not assessed | Verify the eligibility tool is called and that other requirements are distinguished. |
| 3 | What is the total fee for CS101 and AI202, plus the maximum late fee? | Not run | Not run | Not assessed | Expected arithmetic from sample data: 12,000 + 18,000 + 2,000 = 32,000. |
| 4 | And if I pay only 5 days late instead? | Not run | Not run | Not assessed | Verify history resolution and arithmetic: 30,000 + (5 × 100) = 30,500. |
| 5 | What is the capital of France? | Not run | Not run | Not assessed | The agent must honor `NO_MATCH` rather than answer from general knowledge. |

## Model and embeddings

Configured defaults from `.env.example` (not runtime-tested):

| Setting | Value |
|---|---|
| Chat provider | `ollama` |
| Chat model | `qwen2.5:1.5b` |
| Embedding provider | `ollama` |
| Embedding model | `nomic-embed-text` |

The code also supports Groq-compatible chat through `GROQ_API_KEY`, FastEmbed
embeddings, and a deterministic offline hash embedder (`EMBED_PROVIDER=hash`).

## Relevance threshold

The code's provisional default is `MAX_DISTANCE=0.75` using Chroma cosine
distance (smaller is more similar). It is configurable in `.env`. No score
measurements are available yet, so this is a starting value, not an empirically
validated threshold. Use the `2_search.py` scores and the assessment agent's
relevant/irrelevant query score output to compare known handbook questions with
out-of-scope questions. Adjust `MAX_DISTANCE` only after inspecting those
scores; rerun the France query to confirm it returns `NO_MATCH` while handbook
queries still pass.

## Limitations and improvements

- Tool-call compliance depends on the selected model and its tool-calling
  support; the five-turn run must be inspected rather than assumed successful.
- The default Ollama model and embedding server must be installed, running, and
  have the configured models pulled locally.
- Cosine distance and the selected cutoff are model-dependent.
- Hash embeddings are an offline demonstration fallback and are not a substitute
  for semantic embeddings.
- Sample policy and fee data are educational examples, not institutional advice.
