# AI Repo Intelligence Agent

An AI-powered codebase assistant that enables developers to connect a GitHub repository and ask questions about the codebase using natural language. Instead of manually searching through files, developers can ask questions like "Where is authentication implemented?" or "How does the login flow work?" and receive intelligent answers grounded in the actual code.

## Features

- **Smart Code Retrieval**: Uses RAG (Retrieval-Augmented Generation) to find relevant code snippets
- **Natural Language Queries**: Ask questions in plain English without needing to know the codebase
- **LangGraph Workflow**: Structured reasoning pipeline for consistent, explainable answers
- **File References**: Every answer includes the specific files used to generate the response
- **Modern UI**: Clean Streamlit interface with gradient design and smooth animations
- **GitHub Integration**: Clone and index any public GitHub repository
- **Vector Search**: Semantic search using embeddings for concept-based retrieval
- **Code-Aware Chunking**: Intelligently splits code into manageable chunks with metadata

## How It Works

1. **Repository Ingestion**: Clone a GitHub repository and scan for supported source files (.py, .js, .ts, .jsx, .tsx, .json, .yaml, .md)
2. **Chunking**: Split code into smaller, semantically meaningful chunks with metadata (file path, language)
3. **Embeddings**: Convert each chunk into vector representations using sentence transformers
4. **Vector Storage**: Store embeddings in FAISS for fast similarity search
5. **Query Processing**: When you ask a question, LangGraph analyzes it and retrieves relevant code chunks
6. **Answer Generation**: An LLM uses the retrieved context to generate accurate, file-referenced answers

## Technology Stack

- **Backend**: Python, FastAPI, LangGraph, LangChain
- **RAG**: HuggingFace embeddings, FAISS vector store, sentence-transformers
- **Frontend**: Streamlit with custom CSS styling
- **Orchestration**: LangGraph for structured agent workflows
- **API**: RESTful API with Pydantic validation

## Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd ai-repo-intelligence

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your HF_TOKEN and GITHUB_TOKEN (optional)
```

## Usage

### Start the Backend API

```bash
source .venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend API will be available at `http://localhost:8000`

### Start the Streamlit Frontend

In a new terminal:

```bash
source .venv/bin/activate
streamlit run streamlit_app.py
```

The frontend will be available at `http://localhost:8501`

### Using the Application

1. Open the Streamlit app in your browser
2. Enter a GitHub repository URL in the sidebar (e.g., `https://github.com/username/repo`)
3. Wait for the repository to be processed and indexed
4. Start asking questions about the codebase:
   - "Where is authentication implemented?"
   - "How does the login flow work?"
   - "Why might this endpoint return 401?"
   - "Where is the database connection configured?"
5. View answers with referenced file paths for context

## API Endpoints

- `POST /api/v1/upload-repo` - Upload and index a GitHub repository
- `POST /api/v1/chat` - Ask questions about the indexed repository
- `GET /` - Health check endpoint

## Example Questions

- Where is authentication implemented?
- How does the login flow work?
- Why might this endpoint return 401?
- Where is the database connection configured?
- Which files handle user registration?
- What happens after a user submits the login form?

## Project Structure

```
ai-repo-intelligence/
├── app/
│   ├── api/          # FastAPI routes and endpoints
│   ├── config/       # Configuration and settings
│   ├── graph/        # LangGraph workflow and nodes
│   ├── ingestion/   # Repository cloning and processing
│   ├── llm/          # LLM client and prompts
│   └── retrieval/    # Embeddings and vector store
├── data/             # Vector store and temporary files
├── main.py           # FastAPI application entry point
├── streamlit_app.py  # Streamlit frontend
└── requirements.txt  # Python dependencies
```

## Configuration

Edit `.env` file to configure:
- `HF_TOKEN`: HuggingFace API token for LLM access
- `HF_MODEL`: Model ID (default: zai-org/GLM-5.3)
- `GITHUB_TOKEN`: GitHub token for private repositories (optional)

## License

MIT License - See LICENSE file for details
