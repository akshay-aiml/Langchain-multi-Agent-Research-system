# LangChain Multi-Agent Research System

A lightweight LangChain-based multi-agent research pipeline that combines web search, URL scraping, report writing, and critique into a single experimental workflow.

The repository demonstrates how to wire LangChain agents, Groq LLM integration, and custom tool wrappers into a reusable research automation pipeline.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Setup](#setup)
- [Running the Project](#running-the-project)
- [Environment Variables](#environment-variables)
- [Developer Experience](#developer-experience)
- [LangChain Workflow](#langchain-workflow)
- [Files and Entry Points](#files-and-entry-points)
- [Notes](#notes)

---

## Project Overview

This project is built around a research pipeline that uses two LangChain agents plus prompt templates to:

- discover topical content using a web search tool,
- scrape and extract readable website text,
- synthesize a structured research report,
- critique the report for improvements.

It is designed as a minimal proof-of-concept for multi-agent workflows integrating external tools and LLM chains.

---

## Key Features

- `LangChain` agent orchestration with custom tools
- `ChatGroq` LLM integration via `langchain-groq`
- web search tool powered by `Tavily`
- robust URL scraping with `trafilatura`, `readability-lxml`, and `BeautifulSoup`
- prompt-driven writer and critic chains
- Streamlit app scaffold for future UI development
- simple CLI/demo entrypoint in `main.py`

---

## Architecture

The repository is organized into a compact, opinionated structure:

- `src/agents/agents.py`
  - Builds the search and reader agents using `langchain.agents.create_agent`
  - Defines the writer and critic prompt chains using `ChatPromptTemplate`
  - Uses `StrOutputParser` to normalize LLM output

- `src/tools/tools.py`
  - Defines `web_search` and `scrape_url` as LangChain tools with `@tool`
  - Uses `TavilyClient` for web search results
  - Uses a multi-strategy scraping approach for robust content extraction

- `src/pipelines/pipeline.py`
  - Orchestrates the research workflow end-to-end
  - Invokes the search agent, then the reader agent, then the writer and critic chains
  - Combines results into a final `state` dictionary

- `app.py`
  - Streamlit page configuration and custom theming
  - Provides a ready-to-style UI shell for research pipeline presentation

- `main.py`
  - Minimal demo runner that launches the pipeline for a sample topic

---

## Setup

### 1. Create and activate a Python virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 3. Create your `.env`

Copy or create a `.env` file in the project root with the required API keys.

Example `.env`:

```env
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

> Do not commit your `.env` file. Keep secrets out of version control.

---

## Running the Project

### Run the pipeline from the command line

```bash
python main.py
```

This executes the `run_research_pipeline` function from `src/pipelines/pipeline.py` with a sample topic.

### Run the Streamlit interface

```bash
streamlit run app.py
```

The Streamlit entrypoint currently contains page configuration and theme styling for a dark UI shell.

---

## Environment Variables

The project depends on two external service keys:

- `GROQ_API_KEY` — required for the `ChatGroq` LLM backend
- `TAVILY_API_KEY` — required for the `TavilyClient` search tool

If these values are missing, the agents will fail to instantiate or call the external APIs.

---

## Developer Experience

### Recommended workflow

1. Activate the virtual environment.
2. Install or update dependencies from `requirements.txt`.
3. Configure `.env` with valid API keys.
4. Run `python main.py` for validation.
5. Run `streamlit run app.py` for UI experimentation.

### Useful checks

- `python -m pip install -r requirements.txt`
- `python -m py_compile main.py src/agents/agents.py src/tools/tools.py src/pipelines/pipeline.py`

### Future improvements

- add Streamlit UI form controls and result cards
- add robust validation for missing env variables before agent build
- add caching for repeated search / scrape requests
- add unit tests for tools and pipeline orchestration

---

## LangChain Workflow

This project uses LangChain in two main ways:

1. **Agent + Tool orchestration**
   - `build_search_agent()` creates a LangChain agent with the `web_search` tool.
   - `build_reader_agent()` creates a second agent with the `scrape_url` tool.
   - Both agents are built with the same `ChatGroq` LLM instance.

2. **Prompt chains**
   - `writer_chain` uses a `ChatPromptTemplate` to generate a structured research report.
   - `critic_chain` uses a second prompt template to score and review the generated report.

The end-to-end flow is:

- user topic → search agent → search results
- search results → reader agent → scraped article text
- combined research → writer chain → report
- report → critic chain → analysis / score

This model is a pure LangChain pipeline rather than a full LangGraph graph architecture.

---

## Files and Entry Points

- `requirements.txt` — project dependencies
- `.env` — local API credentials (not committed)
- `app.py` — Streamlit UI shell and custom theme styles
- `main.py` — demo runner for the research pipeline
- `src/agents/agents.py` — LangChain agent bindings and prompt chains
- `src/tools/tools.py` — web search and URL scraping tools
- `src/pipelines/pipeline.py` — pipeline orchestration

---

## Notes

- The repository is intentionally minimal and aims to illustrate a multi-agent research orchestration.
- The current code uses `ChatGroq` with `llama-3.3-70b-versatile` as the default model.
- Scraping results are truncated to the first 5000 characters for reliability.
- The Streamlit app currently includes styling and configuration but can be extended with interactive controls.

---

## License

This repository is suitable for open-source distribution. 
