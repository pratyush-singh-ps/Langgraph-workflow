# AI Agent Platform

This project is a modular AI agent that accepts user prompts, leverages a knowledge base, and integrates with tools for API calls and database extraction.

## Features
- Accepts user prompts via API or CLI
- Integrates with OpenAI LLM
- Uses a knowledge base for context-aware answers
- Extensible tool interface for APIs, databases, and more

## Setup
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure your API keys and environment variables in `.env` or `config/config.yaml`

## Run (API Example)
```bash
uvicorn main:app --reload
```

## Folder Structure
- `main.py` - Entry point
- `agent/` - Core agent logic
- `knowledge_base/` - Knowledge ingestion & retrieval
- `tools/` - Tool interfaces & adapters
- `llm/` - LLM integration
- `config/` - Configuration files 
