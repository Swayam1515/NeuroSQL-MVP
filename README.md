# NeuroSQL Intelligent System (NL2SQL MVP)

NeuroSQL is an advanced, production-grade Natural Language to SQL (NL2SQL) translation system built as a multi-model FastAPI application. Designed to bridge the gap between non-technical stakeholders and complex relational databases, NeuroSQL interprets natural language prompts to intelligently query internal data structures natively and safely—featuring a visually stunning glassmorphism dashboard.

## System Architecture

NeuroSQL is built around several isolated modules to ensure data security and LLM flexibility:
1. **Core Translation Layer (Vanna AI 2.0):** Leverages `vanna[sqlite]` to handle memory context and agent generation states.
2. **Dual-LLM Support:** Dynamic router enabling users to execute queries against either **Gemini 2.5 Flash** or **Z.ai GLM 4.5 Flash**.
3. **Regex Extraction Middleware:** To bypass standard LLM tool-calling limits, a robust custom streaming aggregator captures and filters ` ```sql ... ```` blocks accurately.
4. **Validation Security Wrapper:** Implements `ValidatedSqliteRunner`, a wrapper over Vanna's built-in sqlite runner, which intercepts and sanitizes queries to block schema alterations, dropping tables, or system executions before they touch the database.
5. **FastAPI Web Service:** The entire ecosystem is deployed securely via standard HTTP endpoints (`/chat`, `/api/upload_db`, `/api/schema`).
6. **"Bring Your Own Database":** Dynamic Python state tracking (`AppState.db_path`) allowing instantaneous runtime SQLite DDL reloads without needing to restart the `uvicorn` server constraints.

## Database Limitations & Setup

- **Supported Format:** This platform supports strictly native **SQLite Databases** (`.db` or `.sqlite`). 
- **Not Supported Formats:** It does **not** natively interpret flat `.csv` files as databases (these must be converted to `.db` first), nor external connected clouds (Postgres, SQL Server).
- **Finding Test Databases:** If you wish to test custom schemas aside from the preloaded `clinic.db`, you can download free `.db` dummy datasets from:
  - [Kaggle SQLite Databases](https://www.kaggle.com/datasets?fileType=sqlite)
  - [SQLite Tutorial Sample DB](https://www.sqlitetutorial.net/sqlite-sample-database/)

## Installation & Startup

🚨 **Important Note on Environment Setup:** Please refer to the **`installguide.md`** file for an ultimate, step-by-step beginner-friendly installation and troubleshooting process.

This system requires **Python 3.10 to 3.13**. Make sure your python and pip environments match. DO NOT use Python 3.14+ to prevent `pandas` C++ build errors!

### 1. Environment Preparation
Running within a virtual environment is highly recommended to avoid dependency conflicts:
```bash
# 1. Create a virtual environment
python -m venv venv

# 2. Activate the virtual environment
source venv/bin/activate    # For Linux / Mac
# .\venv\Scripts\activate   # For Windows

# 3. Install Requirements
python -m pip install -r requirements.txt

# 4. Install Missing Database Drivers
python -m pip install "vanna[openai,sqlite]"
```
*(If you must run globally, append `--break-system-packages` to the pip commands).*

### 2. Environment Variables (`.env`)
Ensure you have an active `.env` file generated at the root of the directory providing API access:
```env
GOOGLE_API_KEY="AIzaSy..."
ZAI_API_KEY="db45..."
```

### 3. Execution

We built an intelligent launcher, but for safety and robust logging across all systems without silent failures, we recommend directly launching the FastAPI web application manually:

```bash
# Spin up FastAPI directly safely
python -m uvicorn main:app --port 8000
```
Then, access the application via your browser at **http://127.0.0.1:8000/**.

*(Alternatively, you can run the original console batched tester via `python generate_results.py` and select Option 1).*
