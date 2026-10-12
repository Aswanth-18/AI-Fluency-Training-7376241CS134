# Scholarship and Student Financial Support Helpdesk

A sample RAG and LangGraph project for answering student scholarship,
examination, fee, hostel, library, and AI fluency training questions. Every
policy in `data/` is illustrative sample-college data, not a real institution's
rules.

## Requirements

- Windows PowerShell
- Python 3.10 or newer
- Ollama for the default local chat and embedding configuration, or a Groq
  compatible API key for hosted chat

## Setup (Windows PowerShell)

From the `assessment_ps_1` directory:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` to change local model settings. Do not put real keys in source
files, screenshots, or committed files. `.env` is ignored by Git.

### Ollama (default)

Install Ollama for Windows and start it. Then pull the configured chat and
embedding models:

```powershell
ollama pull qwen2.5:1.5b
ollama pull nomic-embed-text
```

Make sure the Ollama service is running before invoking the Python programs.
The model must support tool calling for the agent demos; if it does not, select
a compatible model and update `MODEL` in `.env`.

### Groq-compatible hosted chat

Keep `EMBED_PROVIDER=ollama` (or choose `fastembed` or `hash`) and set the
following values in your local `.env`:

```text
PROVIDER=groq
MODEL=<a tool-calling model available to your account>
GROQ_API_KEY=<your key>
```

You can edit `.env` in VS Code without putting the key in a command, source
file, or shell history. The default API base is
`https://api.groq.com/openai/v1`; set `GROQ_BASE_URL` in `.env` only if using
another compatible service. Never commit `.env`.

For embeddings without an Ollama embedding service, set
`EMBED_PROVIDER=fastembed` and choose an available FastEmbed model in
`EMBED_MODEL`. FastEmbed may need to download its model the first time. For a
network-free demonstration, `EMBED_PROVIDER=hash` uses deterministic feature
hashes; its semantic retrieval quality is limited.

## Run in order

Run these commands from the project directory after activating `.venv`:

```powershell
python 1_ingest.py
python 2_search.py
python 3_rag_chain.py
python 4_graph_basics.py
python 5_agentic_rag.py
python task_agent.py
```

`1_ingest.py` creates `chroma_db/`, which is excluded from Git. Re-run
ingestion after changing the source documents or embedding configuration.
Changing embedding models requires rebuilding the database.

To capture the assessment output in `run_log.txt`:

```powershell
python task_agent.py 2>&1 | Tee-Object -FilePath run_log.txt
```

The Chroma distance threshold is controlled by `MAX_DISTANCE` in `.env`
(default `0.75`). Chroma is configured for cosine distance, where smaller values
are more similar. Thresholds depend on the embedding model; inspect relevant
and irrelevant query scores from `2_search.py` and `task_agent.py` and tune
against observed results. Do not treat the default as validated before
measuring it. Search results print source filenames and short passages.

## Troubleshooting

- **Ollama connection errors:** Start the Ollama application/service, confirm
  the local API is reachable, and verify that the model names in `.env` match
  models shown by `ollama list`.
- **Missing Python packages:** Activate the project `.venv` and run
  `pip install -r requirements.txt` again.
- **Model tool-calling limitations:** `5_agentic_rag.py` and `task_agent.py`
  need a LangChain chat model that supports tool calling. Select a supported
  Ollama or Groq model and check its provider documentation.
- **Missing Chroma database:** Run `python 1_ingest.py` before either search
  script. If using a different embedder, re-ingest with that embedder.
- **Relevance threshold rejects useful queries:** Review distances printed by
  search, then raise `MAX_DISTANCE` carefully and retest both relevant and
  irrelevant questions. Larger cutoffs accept more matches.
- **PowerShell activation errors:** For the current PowerShell session only,
  you can allow activation scripts with
  `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`, then run
  `.\.venv\Scripts\Activate.ps1`. Alternatively invoke
  `.\.venv\Scripts\python.exe` directly.

## Files

- `lc_config.py`: project-relative configuration, providers, embeddings, and
  Chroma setup.
- `1_ingest.py`, `2_search.py`, `3_rag_chain.py`: ingestion, search, and RAG.
- `4_graph_basics.py`, `5_agentic_rag.py`: LangGraph routing and basic tool
  agent.
- `task_agent.py`: the four-tool, five-question assessment.
- `results.md`: record actual measurements and model run results.
- `screenshots/README.md`: capture checklist.
