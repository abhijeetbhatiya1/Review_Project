# 📝 Customer Feedback Analyzer

A local, privacy-first AI sentiment analysis system for customer reviews. This project features a FastAPI microservice backend powered by **Ollama**, a SQLite database for history tracking, and a Streamlit dashboard frontend.

---

## 🏗️ Project Architecture

The app is structured into three clean layers:
* 🖥️ **Frontend ([app.py](app.py))**: A Streamlit dashboard where users paste customer reviews, view sentiment metrics, and save history.
* ⚙️ **Backend ([api.py](api.py))**: A FastAPI microservice that uses Ollama to perform structured JSON sentiment analysis.
* 💾 **Database ([database.py](database.py))**: SQLite storage layer that creates and manages the local database (`feedback.db`).

---

## 📦 Dependencies

The project requirements are defined in [pyproject.toml](pyproject.toml) and managed using `uv`:
* 🎈 **Streamlit (v1.58.0)** — Frontend UI framework
* ⚡ **FastAPI (>=0.136.3)** & **Uvicorn (v0.40.0)** — High-performance backend & web server
* 🦙 **Ollama (v0.6.1)** — Local LLM integration
* 🛡️ **Pydantic (>=2.13.4)** — Schema and type enforcement
* 🔗 **Requests (>=2.34.2)** — Communication between frontend and backend
* 🗄️ **ChromaDB (v1.4.1)** & **Python-dotenv (>=1.2.2)** — Database & local config management

---

## 🚀 How to Run the Project

### 1️⃣ Run the Local AI Engine
Ensure **Ollama** is running locally and pull the target model (we use `llama3.2:3b` as a reference, but you can use any compatible model you want):
```bash
ollama pull llama3.2:3b
```

### 2️⃣ Install Dependencies
Synchronize project packages using `uv`:
```bash
uv sync
```

### 3️⃣ Start the Backend Microservice
Run the FastAPI backend (in your first terminal):
```bash
uv run fastapi dev api.py
```
*The service will start at `http://127.0.0.1:8000`.*

### 4️⃣ Start the Frontend Dashboard
Run the Streamlit frontend (in a second terminal):
```bash
uv run streamlit run app.py
```
*The dashboard will automatically open in your browser!* 

---

## 🧠 Local AI Model Details
This project runs entirely offline using the **`llama3.2:3b`** model via Ollama. 
The backend parses each review and returns structured JSON containing:
* **Label**: `positive` 😊, `neutral` 😐, or `negative` 😡
* **Score**: `1` (Very Bad) to `5` (Very Good) ⭐
* **Theme**: One-word topic categorization (e.g., `delivery`, `price`, `service`) 🏷️