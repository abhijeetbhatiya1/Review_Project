# 📝 Customer Feedback Analyzer

A lightweight, privacy-first, and completely local AI-powered sentiment analysis system for customer reviews. This project decouples the architecture into a **Streamlit** frontend dashboard, a **FastAPI** microservice backend, an **Ollama** local LLM engine (`llama3.2:3b`), and a **SQLite** database for persistent storage.

---

## 🏗️ Project Architecture

The project is structured into three clean layers to ensure separation of concerns:

```text
├── api.py       # FastAPI microservice (Structured JSON generation via Ollama)
├── app.py       # Streamlit dashboard (Frontend UI, batch handling & metrics)
├── database.py  # SQLite database layer (Data persistence and history tracking)
└── feedback.db  # Generated local SQLite database file

## 🚀 How to Run the App (Quick Start)

Because the project features a fully unified pipeline, you do not need to manage multiple terminal tabs or manually coordinate background processes. The single-file entry script handles process orchestration automatically.

Follow this exact terminal sequence:

### 1. Run your Local AI Engine
Ensure Ollama is running in the background and pull your model to verify it's active:
```bash
ollama pull llama3.2:3b

### 2. Install Project Dependencies
check Dependencies in **pyproject.toml** file.
```bash
uv sync

### 3. Launch the Application
Execute the unified app script from your main project folder. This single command will silently initialize the SQLite database table, boot your FastAPI background worker, and launch your Streamlit UI dashboard interface:

```bash
uv run combined_app.py

### 4. Stopping the Stack
When you are done testing, simply press Ctrl + C inside your terminal window to cleanly kill both the frontend and background backend processes simultaneously.

***

### 💡 One Quick Adjustment
If you are replacing the previous setup instructions with this, make sure the top file tree visualization in your `README.md` simply shows your new single-file name (like `combined_app.py`) so your documentation stays perfectly synchronized with your workspace!
***