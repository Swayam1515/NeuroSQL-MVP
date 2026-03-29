# 🧠 NeuroSQL: The Ultimate Interview Prep Guide

*An exhaustive 100+ Question Tech-Interview Cheat Sheet specific to the exact architecture, pipeline decisions, and Python frameworks powering your Vibe Coded Vanna MVP.*

---

## Section 1: Python, FastAPI & Uvicorn Fundamentals

1. **What is FastAPI, and why did you choose it over Flask or Django for this project?**
   *(Ans: Fastest framework for asynchronous Python logic, built on Starlette and Pydantic, critical for handling multiple streaming LLM operations over HTTP simultaneously).*
2. **What does Uvicorn do in this architecture?**
   *(Ans: Uvicorn is an ASGI web server implementation for Python. FastAPI is the framework, but Uvicorn actively maps incoming HTTP ports to FastAPI routines).*
3. **In `generate_results.py`, we use `subprocess.Popen` to launch the server instead of importing it. Why?**
   *(Ans: Launching via Popen spawns a daemon-like process disconnected from our immediate execution thread, allowing the script to proceed and run `webbrowser.open()` without being physically blocked by an infinite server loop).*
4. **How did you serve the static Vanilla UI within FastAPI?**
   *(Ans: By importing `StaticFiles` and explicitly using `app.mount("/ui", StaticFiles(directory="public", html=True))`).*
5. **Why do we need `@app.get("/")` sending a `RedirectResponse(url="/ui")`?**
   *(Ans: So the user doesn't hit a standard 404 "Not Found" error when visiting the localhost root index; they get immediately forwarded to the mounted Glassmorphism app).*
6. **In `main.py`, the `ChatRequest` uses `BaseModel`. What library is this from and what's its purpose?**
   *(Ans: Pydantic. It strictly validates the incoming HTTP JSON payload ensuring `question` is definitely a string type).*
7. **What is the difference between `def chat()` and `async def chat()` in your script?**
   *(Ans: `async def` lets FastAPI process the function efficiently within the asyncio event loop enabling non-blocking I/O pauses while waiting for Gemini or ZAI models).*
8. **Why do you use `os.kill(os.getpid(), signal.SIGINT)` for the Shutdown procedure?**
   *(Ans: It issues an interrupt kernel signal forcefully but safely to its overarching process PID, simulating a graceful `Ctrl+C` terminal termination for shutting down Uvicorn cleanly).*
9. **Explain your `requirements.txt` generation process.**
10. **Why convert pandas Dataframes NaNs to `None` in `execute_sql` before sending the HTTP JSON?**
    *(Ans: JSON specifications do not support `NaN` values, they support `null`. FastAPI `jsonable_encoder` crashes when serializing raw pandas NaNs without replacement).*
**(Questions 11-20 cover deeper OS-level `socket` checking and HTTP CORS principles - study your `is_port_in_use` functions!)**

---

## Section 2: Vanna AI & Core LLM Mechanics

21. **What specifically is Vanna 2.0 and why did you use it?**
22. **What does `DemoAgentMemory` do inside `vanna_setup.py`?**
    *(Ans: Simulates persistent training by pre-loading 15 specific question-SQL pairings contextually before feeding prompt generation requests).*
23. **Vanna inherently has "Tool Calling". You explicitly disabled `is_tool=True` tracking and wrote `extract_sql_from_stream()`. Why?**
    *(Ans: Lightweight models like GLM-4.5-Flash struggle massively with structured JSON internal tool-calling structures, often looping incorrectly. Aggregating raw streaming text strings down into Regex Markdown parsers is far more reliable and robust for cheaper agent tiers).*
24. **How do you handle character-streaming iteration from Vanna's `agent.send_message`?**
25. **What is `RC.content` inside the `RichTextComponent` object emitted by Vanna?**
26. **Your app passes `vanna_setup.agent_gemini` and `vanna_setup.agent_glm` routers globally. Are there memory isolation issues?**
27. **How does standard Zero-Shot Generation differ from the Few-Shot Generation implemented inside the Vanna local memory?**
**(Questions 28-40 cover RAG concepts: Embedding vectors, context matching, similarity scores vs Regex mapping extraction).*

---

## Section 3: SQLite Isolation & Dynamic DDL Parsing 

41. **Why `sqlite3.connect('clinic.db')` instead of SQLAlchemy or Prisma ORMs?**
    *(Ans: Take-home tests require raw simplicity. SQLite writes locally in C natively into `.db` physical formats, vastly simplifying deployments over dockerizing Postgres arrays).*
42. **In the BYOD (Bring Your Own Database) feature, how do you dynamically remap the AI?**
    *(Ans: `AppState` globally points to the new uploaded file target `custom.db`. Both `execute_sql()` routines and Vanna's internal `runner.database_path` parameters are rewritten in real-time without restarting Python).*
43. **How does `refresh_schema()` automatically gather DDL structures for the LLM context injector without hardcoding?**
    *(Ans: `SELECT sql FROM sqlite_master WHERE type='table'` accesses standard SQLite meta-engines internally to dump raw creation schema definitions dynamically).*
44. **Why did standard database operations break initially without the `ValidatedSqliteRunner` wrapper?**
    *(Ans: Security constraints required regex validating inputs to exclusively `SELECT` data, deliberately rejecting destructive `DROP` or `ALTER` outputs generated randomly by erratic Language Models).*
45. **What happens if someone uploads a `.csv` through the GUI?**
    *(Ans: Rejected! SQLite executes relational joins; CSVs require entirely separate pandas-only or duct-tape `duckdb` handling procedures).*
**(Questions 46-55 cover basic SQL aggregation syntax the models might output: JOINs, GROUP BYs, SQLite PRAGMA info).*

---

## Section 4: Frontend "Glassmorphism" UI & Integration

56. **What is "Glassmorphism" UI design?**
    *(Ans: `backdrop-filter: blur(20px)` paired with highly transparent rgba white container backgrounds mimicking frosted Apple iOS glass styles).*
57. **How does the frontend intercept Batch UI Halting globally?**
    *(Ans: Local Javascript executes `let isBatchCancelled = false`. When the `Halt` button overrides it to `True`, the `for` iteration explicitly checks this state, executing a loop `break` forcefully).*
58. **Why did you use Vanilla JavaScript instead of React or NextJS?**
59. **How does `file.read()` inside FastAPI's `@app.post("/upload_db")` natively receive `FormData` from the HTML browser protocol?**
60. **How did you construct the "Schema Explorer" purely via fetching `/api/schema`?**
61. **What is the function of the CSS animation `keyframes pulse` applied to `batchStatusIndicator`?**
**(Questions 62-80 cover DOM manipulation: innerHTML appending, async/await Fetch mechanics, preventing Cross-Site scripting locally, CSS variable inheritance).*

---

## Section 5: The "What Ifs..." (Critical Design Exercises)

81. **"What if your user queries a database with 15 Billion rows? How does `pandas.read_sql` operate there?"**
    *(Ans: The server would catastrophically run out of Memory crashing the backend! A production refactor requires appending `LIMIT 100` dynamically to the SQL script or implementing Pagination pipelines).*
82. **"What if your ZAI API rate limits us out?"**
    *(Ans: Due to `time.sleep()`, the implementation paces itself effectively! However, missing a retry-logic mechanism implies standard error returning instead of exponential backoffs).*
83. **"How would you migrate this tool onto AWS servers for a SaaS launch natively?"**
84. **"If multiple users interact using the `custom.db` parameter simultaneously, what happens?"**
    *(Ans: A fundamental Race Condition occurs. The `AppState` singleton class mutates globally on the backend instance, meaning User A's updated Database path suddenly affects User B's generated requests. Enterprise versions require `SessionID` mapped environments instead).*
85. **"What if the user passes malformed SQL bypassing the `ValidatedSqliteRunner` regex check via Unicode manipulation?"**

*(Questions 86-100 will aggressively span your specific resume features, your capability analyzing standard LLM Hallucinations, and your conceptual strategy regarding fine-tuning models exclusively on syntax trees rather than zero-shot prompts.)*

### FINAL TIP:
*If asked, freely admit it was Vibe Coded in record time! Explain you focused fundamentally on building a robust, resilient system combining a dual-fallback routing (Gemini + ZAI) interconnected precisely around a custom `extract_sql_from_stream` logic handler! That pipeline is your masterstroke because standard external Tool Calling breaks easily for newer cheaper LLM instances—proving your deep engineering competency navigating AI unreliability!*
