# Screenshot checklist

Capture genuine screenshots after running the programs. Do not add mock or
fabricated output.

- **Ingestion output:** terminal output from `python 1_ingest.py`, showing the
  document, chunk, and stored-vector counts.
- **Search output:** terminal output from `python 2_search.py`, including
  scores, sources, and passages.
- **Agent tool calls and answers:** terminal output from `python task_agent.py`
  showing tool calls and all five responses in the shared conversation thread.
- **Relevance-guard test:** relevant handbook query scores and the out-of-scope
  France query, including whether the guard returns `NO_MATCH`.

Avoid capturing API keys, access tokens, or other private information.
