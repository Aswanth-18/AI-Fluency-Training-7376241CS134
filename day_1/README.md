# AI Fluency Training — Roll No: 7376241CS134

Repository containing assignments and assessment tasks for the **AI Fluency Training** program.

---

## Repository Structure

```text
AI-Fluency-Training-7376241CS134/
│
├── assessment_day_1/
│   │
│   ├── chatbot/
│   │   └── chatbot.py
│   │
│   ├── rule_based/
│   │   └── workflow.py
│   │
│   ├── agent/
│   │   ├── agent.py
│   │   ├── config.py
│   │   └── tools.py
│   │
│   ├── Output/
│   │   ├── Screenshot 2026-09-21 212441.png
│   │   ├── Screenshot 2026-09-21 212544.png
│   │   ├── Screenshot 2026-09-21 212710.png
│   │   ├── Screenshot 2026-09-21 212821.png
│   │   ├── Screenshot 2026-09-21 213310.png
│   │   └── Screenshot 2026-09-21 213428.png
│   │
│   └── analysis.md
│
├── .gitignore
└── README.md
```

---

## Day 1 Assessment Overview

This assessment compares three paradigms of software automation and AI integration for college course fee queries:
1. **System 1: LLM Chatbot (`chatbot/chatbot.py`)** — Pure language model relying solely on its internal training weights.
2. **System 2: Rule-Based Workflow (`rule_based/workflow.py`)** — Deterministic regex and lookup dictionary without LLM reasoning.
3. **System 3: AI Agent (`agent/agent.py`)** — Hybrid system leveraging OpenAI/Groq function calling with external tools (`get_course_fee` and safe AST `calculator`).

For in-depth architectural and benchmark comparison, see [analysis.md](file:///assessment_day_1/analysis.md).

---

## Prerequisites & Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Aswanth-18/AI-Fluency-Training-7376241CS134.git
   cd AI-Fluency-Training-7376241CS134
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   # Windows PowerShell
   .venv\Scripts\Activate.ps1
   # Linux/macOS
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file with your preferred provider and API key:
   ```env
   PROVIDER=groq
   GROQ_API_KEY=your_groq_api_key_here
   MODEL=openai/gpt-oss-20b
   ```

---

## How to Run

### 1. Chatbot (System 1)
```bash
python assessment_day_1/chatbot/chatbot.py
```

### 2. Rule-Based Workflow (System 2)
```bash
python assessment_day_1/rule_based/workflow.py
```

### 3. AI Agent (System 3)
```bash
python assessment_day_1/agent/agent.py
```

---

## Output Screenshots
All terminal output captures and test runs are preserved inside the [`assessment_day_1/Output/`](file:///assessment_day_1/Output/) folder.
