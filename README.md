# Local Ollama AI model 

An intro project on Python that uses a local LLM model (Phi-4 via Ollama) to create and process requests and work text notes.
The assistant program can:
- Answer questions and create notes
- Rewrite and improve your existing notes
- Summarize existing notes entries
- Answer questions based on existing notes content

Runs entirely offline — no internet, no cloud, no data leaks. Your data stays private and a local model maintains the fastest response times.

## Project Structure

```
local/
├── main.py
├── client.py           # Wrapper for interacting with local Ollama
├── notes.txt           # Context notes and summary (auto-generated and manually editable)
├── log.txt             # Full conversation history log (auto-generated)
├── requirements.txt
└── prompts/            # Prompt templates for each mode
    ├── summarize.txt
    ├── question.txt
    └── rewrite.txt
```

## Features

Context system is **editable knowledge base** as `notes.txt`. After each question, the model appends a **summary line**. You can edit or delete lines to refine the assistant’s context. Each interaction dumped in `log.txt` which contains **all full replies and questions**, formatted for clarity.

| Feature     | Description                                 |
|-------------|---------------------------------------------|
| `summarize` | Summarizes your notes                       |
| `rewrite`   | Rewrites text to make it clearer or nicer   |
| `question`  | Answers questions based on the notes        |

## Roadmap

- [x] Base CLI version
- [x] Mode switching (summarize, question, rewrite)
- [x] Markdown (`.md`) support by regex
- [x] Context logging 
- [x] Full conversation logging
- [ ] GUI with Tkinter or Textual
- [ ] Store notes in SQLite
- [ ] Tag and filter notes

## Steps to run

### 1. Install Ollama and pull the Phi-4 model

```bash
# Install Ollama (https://ollama.com/download)
ollama run phi4
```

### 2. Clone the repository

```bash
git clone https://github.com/account/local.git
cd local
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
python main.py --help

python main.py --mode summarize

python main.py --mode question
"How to cook an egg?"
```
