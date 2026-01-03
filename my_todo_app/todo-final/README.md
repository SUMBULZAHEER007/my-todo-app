# Phase III – AI-Enhanced Todo Backend API

## Overview
This project is Phase III of the "Evolution of Todo App" built using
Spec-Driven Development. Phase III introduces AI/RAG capabilities to the
persistent API-based backend service from Phase II, while preserving all
previous functionality.

## Features
- All functionality from Phase I & II (persistent storage, REST API)
- AI-based task recommendations
- Natural language querying of tasks
- Contextual answers based on user tasks
- AI summaries of completed tasks

## Tech Stack
- Python 3.13+
- FastAPI
- SQLAlchemy
- SQLite (persistent storage)
- LangChain (RAG implementation)
- OpenAI API, Anthropic (Claude), or local models
- Qdrant (vector database)
- Free-tier / open-source tools only

## How to Run the Backend

1. Clone the repository
   ```bash
   git clone <repository-url>
   cd <project-folder>
   ```

2. Create and activate a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables
   ```bash
   # Create a .env file with your API keys:
   OPENAI_API_KEY=your_openai_api_key_here
   # Or to use local models:
   USE_LOCAL_MODEL=true
   # LOCAL_MODEL_PATH=path_to_local_model (if using local models)
   ```

5. Run the API server
   ```bash
   uvicorn my_todo_app.main:app --reload
   ```

6. Open the API docs
   ```
   http://127.0.0.1:8000/docs
   ```

## API Endpoints

### Standard Todo Endpoints
- `POST /todos`
  - Create a new todo
  - Request body: `{"description": "string", "completed": false}`

- `GET /todos`
  - Retrieve all todos
  - Query parameters: `skip` (default 0), `limit` (default 100)

- `GET /todos/{id}`
  - Retrieve a single todo by ID

- `PUT /todos/{id}`
  - Update a todo
  - Request body: `{"description": "string", "completed": false}`

- `DELETE /todos/{id}`
  - Delete a specific todo by ID

- `PATCH /todos/{id}`
  - Update todo completion status
  - Request body: `{"completed": true}`

### AI-Enhanced Endpoints
- `POST /api/chat`
  - Chat with AI about your tasks
  - Request body: `{"query": "your question", "selected_text": "optional context"}`

- `POST /api/tasks/summary`
  - Generate AI summary of all tasks
  - No request body required

## AI Configuration

### Using OpenAI
1. Get an API key from OpenAI
2. Set the `OPENAI_API_KEY` environment variable

### Using Anthropic (Claude)
1. Get an API key from Anthropic
2. Set the `ANTHROPIC_API_KEY` environment variable
3. Set `USE_ANTHROPIC=true`

### Using Local Models (Ollama)
1. Install and run Ollama
2. Pull a model: `ollama pull llama2`
3. Set environment variables:
   ```
   USE_LOCAL_MODEL=true
   LOCAL_MODEL_PATH=/path/to/your/local/model
   ```

### Using Qdrant Vector Database
1. Set up Qdrant (can be local or cloud)
2. Set the `QDRANT_URL` and `QDRANT_API_KEY` environment variables (if using cloud)

## Testing

Run the test script to verify all endpoints work correctly:
```bash
python test_ai_endpoints.py
```

## Notes
- All data is stored persistently in SQLite database.
- The project strictly follows Constitution → Spec → Plan → Tasks → Implement.
- The database file will be created as `todos.db` in the project directory.
- AI features are optional and don't affect existing functionality.
- Natural language processing uses RAG (Retrieval-Augmented Generation) for contextual responses.