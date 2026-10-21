# AI Repo Intelligence Agent

An AI-powered codebase assistant that enables developers to connect a GitHub repository and ask questions about the codebase using natural language. Instead of manually searching through files, developers can ask questions like "Where is authentication implemented?" or "How does the login flow work?" and receive intelligent answers grounded in the actual code.

## 🌟 Features

- **Smart Code Retrieval**: Uses RAG (Retrieval-Augmented Generation) to find relevant code snippets
- **Natural Language Queries**: Ask questions in plain English without needing to know the codebase
- **LangGraph Workflow**: Structured reasoning pipeline for consistent, explainable answers
- **File References**: Every answer includes the specific files used to generate the response
- **Modern UI**: Clean Streamlit interface with gradient design and smooth animations
- **GitHub Integration**: Clone and index any public GitHub repository
- **Vector Search**: Semantic search using embeddings for concept-based retrieval
- **Code-Aware Chunking**: Intelligently splits code into manageable chunks with metadata
- **Multi-turn Chat**: Maintains conversation context for follow-up questions
- **Incremental Updates**: Support for updating vector store with Git diff changes

## 🏗️ Architecture Overview

The application follows a modular architecture with clear separation of concerns:

```
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│   Streamlit     │────────▶│   FastAPI       │────────▶│   LangGraph     │
│   Frontend      │  HTTP   │   Backend       │  Graph  │   Workflow      │
└─────────────────┘         └─────────────────┘         └─────────────────┘
                                                                   │
                                                                   ▼
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│   GitHub Repo   │────────▶│   Code          │────────▶│   FAISS         │
│   (Clone)       │  Files  │   Chunking      │  Embed  │   Vector Store  │
└─────────────────┘         └─────────────────┘         └─────────────────┘
```

## 🔄 How It Works

### Repository Ingestion Pipeline

1. **Repository Cloning** (`app/ingestion/github.py`):
   - User provides a GitHub repository URL
   - The system clones the repository to a temporary directory
   - Supports authentication via GitHub token for private repos

2. **File Scanning** (`app/ingestion/scanner.py`):
   - Scans the cloned repository for supported file types
   - Skips ignored directories (node_modules, .git, __pycache__, etc.)
   - Filters by allowed extensions (.py, .js, .ts, .jsx, .tsx, .json, .yaml, .md)
   - Excludes files larger than 1MB

3. **Code Chunking** (`app/ingestion/chunker.py`):
   - Reads each file and detects the programming language
   - Splits code into smaller, semantically meaningful chunks
   - Uses RecursiveCharacterTextSplitter with configurable chunk size (default: 1000 chars)
   - Adds metadata: file path, language, chunk index
   - Creates overlap between chunks (default: 150 chars) to maintain context

4. **Embedding Generation** (`app/retrieval/embeddings.py`):
   - Converts each chunk into vector representations
   - Uses sentence-transformers/all-MiniLM-L6-v2 model
   - Captures semantic meaning for concept-based search

5. **Vector Storage** (`app/retrieval/vectorstore.py`):
   - Stores embeddings in FAISS (Facebook AI Similarity Search)
   - Generates deterministic chunk IDs (format: `file_path::chunk_index`)
   - Persists to disk for quick loading
   - Supports deletion of chunks by file path for incremental updates

### Query Processing Pipeline (LangGraph)

6. **Question Analysis** (`app/graph/nodes.py` - `analyze_question`):
   - Transforms contextual follow-up questions into standalone search queries
   - Uses LLM to resolve references like "it", "that file", "the second endpoint"
   - Maintains conversation context from chat history
   - Example: "How does it work?" → "How does the authentication system work?"

7. **Code Retrieval** (`app/graph/nodes.py` - `retrieve_code`):
   - Performs semantic search using the reformulated query
   - Retrieves top-k relevant chunks (default: k=5)
   - Uses FAISS similarity search for fast retrieval

8. **Answer Generation** (`app/graph/nodes.py` - `generate_answer`):
   - Passes retrieved code chunks and question to LLM
   - Uses a prompt template that enforces strict grounding in context
   - Generates accurate answers with file citations
   - Includes chat history for multi-turn conversations

## 🛠️ Technology Stack

- **Backend Framework**: FastAPI - Modern, fast web framework for building APIs
- **Orchestration**: LangGraph - Structured agent workflows with state management
- **LLM Integration**: LangChain - Framework for LLM applications
- **Embeddings**: HuggingFace sentence-transformers - State-of-the-art text embeddings
- **Vector Database**: FAISS - Efficient similarity search and clustering
- **Frontend**: Streamlit - Python framework for ML/data apps
- **Git Operations**: GitPython - Python library for Git operations
- **Configuration**: Pydantic Settings - Type-safe configuration management

## 📦 Installation

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

## 🚀 Usage

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

## 🔌 API Endpoints

### POST /api/v1/upload-repo
Upload and index a GitHub repository.

**Request Body:**
```json
{
  "repo_url": "https://github.com/username/repo"
}
```

**Response:**
```json
{
  "message": "Repository successfully processed and indexed.",
  "repo_name": "username_repo",
  "files_processed": 42,
  "chunks_created": 156
}
```

### POST /api/v1/chat
Ask questions about the indexed repository.

**Request Body:**
```json
{
  "question": "Where is authentication implemented?",
  "chat_history": [
    {"role": "user", "content": "Previous question"},
    {"role": "assistant", "content": "Previous answer"}
  ]
}
```

**Response:**
```json
{
  "question": "Where is authentication implemented?",
  "answer": "Authentication is implemented in auth/routes.py...",
  "referenced_files": ["auth/routes.py", "auth/middleware.py"]
}
```

### GET /
Health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "message": "AI Repo Intelligence Agent service running."
}
```

## 📁 Project Structure

```
ai-repo-intelligence/
├── app/                          # Main application package
│   ├── api/                      # FastAPI routes and endpoints
│   │   └── routes.py             # API route handlers for upload and chat
│   ├── config/                   # Configuration management
│   │   └── settings.py           # Pydantic settings with environment variables
│   ├── graph/                    # LangGraph workflow implementation
│   │   ├── graph.py              # Graph construction and compilation
│   │   ├── nodes.py              # Individual workflow nodes (analyze, retrieve, generate)
│   │   └── state.py              # Agent state definition (TypedDict)
│   ├── ingestion/               # Repository ingestion pipeline
│   │   ├── chunker.py            # Code chunking with metadata
│   │   ├── diff_updater.py       # Incremental updates using Git diff
│   │   ├── github.py             # GitHub repository cloning
│   │   └── scanner.py            # File scanning and filtering
│   ├── llm/                      # LLM integration
│   │   ├── client.py             # HuggingFace LLM client initialization
│   │   └── prompts.py            # Prompt templates for RAG
│   └── retrieval/                # Vector storage and retrieval
│       ├── embeddings.py         # Embedding model initialization
│       ├── retriever.py          # Retrieval interface and helper functions
│       └── vectorstore.py        # FAISS vector store management
├── data/                         # Data storage directory
│   ├── vectorstore/              # Persisted FAISS index
│   └── temp_repos/               # Temporary cloned repositories
├── tests/                        # Test suite
│   └── test_chat_route.py        # API route tests
├── .env                          # Environment variables (not in git)
├── .env.example                  # Example environment variables
├── .gitignore                    # Git ignore patterns
├── main.py                       # FastAPI application entry point
├── requirements.txt              # Python dependencies
├── streamlit_app.py              # Streamlit frontend application
├── STREAMLIT_SETUP.md            # Streamlit setup documentation
└── test_script.py                # Test script for manual testing
```

## 📖 Detailed File Explanations

### Core Application Files

#### `main.py`
The FastAPI application entry point. It:
- Initializes the FastAPI app with metadata (title, description, version)
- Includes the API router with `/api/v1` prefix
- Provides a health check endpoint at `/`

**Connection:** This is the starting point for the backend. It imports and mounts the API router from `app/api/routes.py`.

#### `streamlit_app.py`
The Streamlit frontend application. It:
- Provides a modern, gradient-styled UI
- Manages chat history and repository state
- Communicates with the FastAPI backend via HTTP requests
- Displays responses with file references

**Connection:** Communicates with the backend API endpoints defined in `app/api/routes.py`.

### API Layer (`app/api/`)

#### `app/api/routes.py`
Defines the REST API endpoints. It:
- Implements `/upload-repo` endpoint for repository ingestion
- Implements `/chat` endpoint for querying the repository
- Handles request validation using Pydantic models
- Manages error handling and HTTP status codes

**Connections:**
- Uses `app/graph/graph.py` for the LangGraph workflow
- Uses `app/ingestion/github.py` for repository cloning
- Uses `app/ingestion/scanner.py` for file scanning
- Uses `app/ingestion/chunker.py` for code chunking
- Uses `app/retrieval/vectorstore.py` for vector store operations

### Configuration (`app/config/`)

#### `app/config/settings.py`
Centralized configuration management using Pydantic. It:
- Defines all environment variables with types and defaults
- Manages API tokens (HF_TOKEN, GITHUB_TOKEN)
- Configures storage paths (vectorstore, temp directories)
- Sets chunking parameters (chunk size, overlap)
- Defines allowed file extensions and ignored directories
- Provides helper methods to safely read secrets

**Connections:** Used throughout the application by nearly all modules to access configuration values.

### LangGraph Workflow (`app/graph/`)

#### `app/graph/graph.py`
Constructs the LangGraph workflow. It:
- Defines the graph structure with three nodes
- Sets up the execution flow: START → analyze_question → retrieve_code → generate_answer → END
- Compiles the graph into an executable application

**Connections:**
- Imports state from `app/graph/state.py`
- Imports node functions from `app/graph/nodes.py`
- The compiled `graph_app` is used by `app/api/routes.py`

#### `app/graph/nodes.py`
Implements the individual workflow nodes. It contains three main functions:

1. **analyze_question**: Transforms follow-up questions into standalone queries using LLM
2. **retrieve_code**: Performs semantic search using the vector store
3. **generate_answer**: Generates the final answer using retrieved context

**Connections:**
- Uses state from `app/graph/state.py`
- Uses vector store from `app/retrieval/vectorstore.py`
- Uses retriever from `app/retrieval/retriever.py`
- Uses LLM client from `app/llm/client.py`
- Uses prompts from `app/llm/prompts.py`

#### `app/graph/state.py`
Defines the agent state as a TypedDict. It:
- Specifies the structure of data passed between nodes
- Includes: question, chat_history, search_query, retrieved_documents, answer

**Connections:** Used by `app/graph/graph.py` and `app/graph/nodes.py` to maintain workflow state.

### Ingestion Pipeline (`app/ingestion/`)

#### `app/ingestion/github.py`
Handles GitHub repository operations. It:
- Validates and parses GitHub repository URLs
- Clones repositories to temporary directories
- Supports authentication via GitHub tokens
- Cleans up temporary directories after processing

**Connections:**
- Uses settings from `app/config/settings.py`
- Called by `app/api/routes.py` during repository upload

#### `app/ingestion/scanner.py`
Scans cloned repositories for files. It:
- Recursively walks the repository directory
- Filters by allowed file extensions
- Skips ignored directories and large files
- Returns a list of valid file paths

**Connections:**
- Uses settings from `app/config/settings.py`
- Called by `app/api/routes.py` after cloning

#### `app/ingestion/chunker.py`
Splits code files into chunks. It:
- Reads file contents with encoding fallback
- Detects programming language from file extension
- Splits code using RecursiveCharacterTextSplitter
- Adds metadata (file path, language) to each chunk
- Handles encoding errors gracefully

**Connections:**
- Uses settings from `app/config/settings.py`
- Called by `app/api/routes.py` after scanning
- Called by `app/ingestion/diff_updater.py` for incremental updates

#### `app/ingestion/diff_updater.py`
Handles incremental updates using Git diff. It:
- Analyzes Git commits to identify changed files
- Evicts deleted/modified chunks from the vector store
- Re-indexes added/modified files
- Prevents "ghost chunks" (stale embeddings)

**Connections:**
- Uses scanner from `app/ingestion/scanner.py`
- Uses chunker from `app/ingestion/chunker.py`
- Uses vector store functions from `app/retrieval/vectorstore.py`

### LLM Integration (`app/llm/`)

#### `app/llm/client.py`
Initializes the HuggingFace LLM client. It:
- Creates a HuggingFaceEndpoint instance
- Configures model parameters (temperature, max tokens)
- Wraps it in ChatHuggingFace for chat interface

**Connections:**
- Uses settings from `app/config/settings.py`
- Used by `app/graph/nodes.py` for question analysis and answer generation

#### `app/llm/prompts.py`
Defines prompt templates. It:
- Contains the system prompt for the RAG assistant
- Defines the user prompt template with context
- Creates a ChatPromptTemplate that supports chat history
- Enforces strict grounding in provided context

**Connections:**
- Used by `app/graph/nodes.py` in the generate_answer node

### Retrieval System (`app/retrieval/`)

#### `app/retrieval/embeddings.py`
Initializes the embedding model. It:
- Creates a HuggingFaceEmbeddings instance
- Uses the all-MiniLM-L6-v2 model for text embeddings

**Connections:**
- Used by `app/retrieval/vectorstore.py` for creating and loading the vector store

#### `app/retrieval/retriever.py`
Provides retrieval interfaces. It:
- Creates a retriever from a FAISS vectorstore
- Implements similarity search with configurable k
- Provides a helper function for direct chunk retrieval

**Connections:**
- Used by `app/graph/nodes.py` in the retrieve_code node
- Works with FAISS vectorstore from `app/retrieval/vectorstore.py`

#### `app/retrieval/vectorstore.py`
Manages the FAISS vector store. It:
- Generates deterministic chunk IDs (format: `file_path::chunk_index`)
- Creates the vector store from documents with embeddings
- Persists the vector store to disk
- Loads the vector store from disk
- Deletes chunks by file path for incremental updates

**Connections:**
- Uses embeddings from `app/retrieval/embeddings.py`
- Used by `app/api/routes.py` during repository upload
- Used by `app/graph/nodes.py` during query processing
- Used by `app/ingestion/diff_updater.py` for incremental updates

## 🗄️ Data Flow Diagram

### Repository Upload Flow
```
User (Streamlit) → routes.py (/upload-repo)
    → github.py (clone_repository)
    → scanner.py (scan_repository)
    → chunker.py (chunk_files)
    → vectorstore.py (create_vectorstore)
    → github.py (cleanup)
    → Response to User
```

### Chat Query Flow
```
User (Streamlit) → routes.py (/chat)
    → graph.py (graph_app.invoke)
        → nodes.py (analyze_question)
            → llm/client.py (query reformulation)
        → nodes.py (retrieve_code)
            → vectorstore.py (load_vectorstore)
            → retriever.py (retrieve_relevant_chunks)
        → nodes.py (generate_answer)
            → llm/prompts.py (get_rag_prompt_template)
            → llm/client.py (generate answer)
    → Response to User with referenced files
```

## ⚙️ Configuration

Edit `.env` file to configure:

- `HF_TOKEN`: HuggingFace API token for LLM access (required)
- `HF_MODEL`: Model ID (default: zai-org/GLM-5.3)
- `GITHUB_TOKEN`: GitHub token for private repositories (optional)
- `VECTORSTORE_DIRECTORY`: Directory for vector store persistence (default: data/vectorstore)
- `TEMP_CLONE_DIR`: Directory for temporary repository clones (default: data/temp_repos)
- `CHUNK_SIZE`: Code chunk size for embeddings (default: 1000)
- `CHUNK_OVERLAP`: Overlap between code chunks (default: 150)

## 💡 Example Questions

- Where is authentication implemented?
- How does the login flow work?
- Why might this endpoint return 401?
- Where is the database connection configured?
- Which files handle user registration?
- What happens after a user submits the login form?
- How is the user session managed?
- Where are API routes defined?
- What database ORM is being used?
- How are errors handled in this application?

## 🔧 Development

### Running Tests

```bash
pytest tests/
```

### Manual Testing

```bash
python test_script.py
```

## 📝 License

MIT License - See LICENSE file for details
