# AI Repo Intelligence Agent

An AI-powered codebase assistant that lets developers connect a GitHub repository and ask questions about the codebase using natural language.

Instead of manually searching through files, developers can ask questions like:

* Where is authentication implemented?
* How does the login flow work?
* Why might this endpoint return `401`?
* Where is the database connection configured?
* Which files handle user registration?
* What happens after a user submits the login form?

The agent uses **RAG + LangGraph + an LLM** to retrieve relevant code and generate an explanation based on the repository.

---

# Why This Project?

Large repositories can be difficult to understand, especially when:

* You are joining an unfamiliar codebase.
* Documentation is incomplete.
* A feature is implemented across multiple files.
* You need to trace a request through different layers.
* You are debugging code written by someone else.

Traditional keyword search can find files, but it does not explain how the pieces work together.

This project combines code retrieval with an LLM so developers can ask questions in natural language.

---

# MVP Scope

The first version intentionally keeps the system simple.

### MVP supports:

1. Connect a GitHub repository.
2. Clone/download the repository.
3. Read relevant source-code files.
4. Split the code into chunks.
5. Generate embeddings.
6. Store embeddings in a vector database.
7. Retrieve relevant code for a user question.
8. Use an LLM to answer the question.
9. Return the answer with file paths and relevant code context.

### Example

User:

> Where is authentication implemented?

The system may retrieve:

```text
app/auth/routes.py
app/auth/service.py
app/auth/models.py
```

The LLM then explains:

```text
Authentication is mainly implemented in app/auth/.

The login endpoint is defined in app/auth/routes.py.
It calls the authentication service in app/auth/service.py,
which validates the user's credentials.

The JWT token is generated inside the authentication service
after successful credential validation.
```

---

# High-Level Architecture

```text
                 ┌──────────────────────┐
                 │      Developer       │
                 │                      │
                 │ "How does login      │
                 │  flow work?"         │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │     LangGraph       │
                 │       Agent         │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │    Retrieve Code     │
                 │                      │
                 │ Vector Search / RAG  │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │   Relevant Chunks    │
                 │                      │
                 │ auth/routes.py       │
                 │ auth/service.py      │
                 │ auth/models.py       │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │         LLM          │
                 │                      │
                 │ Understand + explain │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │       Answer         │
                 │                      │
                 │ Explanation + file   │
                 │ references           │
                 └──────────────────────┘
```

---

# Repository Ingestion Flow

Before the user can ask questions, the repository needs to be indexed.

```text
GitHub Repository
       │
       ▼
Clone Repository
       │
       ▼
Scan Source Files
       │
       ▼
Filter Unnecessary Files
       │
       ▼
Split Code into Chunks
       │
       ▼
Add Metadata
       │
       ▼
Generate Embeddings
       │
       ▼
Vector Store
```

The vector store becomes the searchable representation of the repository.

---

# What Gets Indexed?

The MVP should focus on source-code files.

For example:

```text
Python
.py

JavaScript
.js

TypeScript
.ts

React
.jsx
.tsx

Other common files
.json
.yaml
.yml
.md
```

Do NOT initially index everything.

Ignore things such as:

```text
.git/
node_modules/
__pycache__/
.env
.venv/
dist/
build/
*.lock
large binary files
```

This keeps ingestion faster and reduces irrelevant retrieval results.

---

# RAG Pipeline

The project uses Retrieval-Augmented Generation.

## 1. Repository ingestion

The repository is scanned and source files are collected.

Example:

```text
backend/
├── auth/
│   ├── routes.py
│   ├── service.py
│   └── models.py
├── users/
│   └── routes.py
└── main.py
```

---

## 2. Chunking

Large source files are divided into smaller chunks.

Each chunk also stores metadata.

Example:

```python
{
    "content": "...authentication code...",
    "file_path": "backend/auth/service.py",
    "language": "python"
}
```

Metadata is important because the final answer should tell the developer where the information came from.

---

## 3. Embeddings

Each code chunk is converted into a vector representation.

```text
Code Chunk
    │
    ▼
Embedding Model
    │
    ▼
Vector
```

Similar concepts produce vectors that are closer together.

For example:

```text
"Where is login implemented?"
```

can retrieve code containing concepts such as:

```text
login()
authenticate_user()
verify_password()
create_access_token()
```

even when the exact word "login" does not appear everywhere.

---

# LangGraph Workflow

LangGraph controls the reasoning workflow.

For the MVP, the graph should remain small.

```text
                  START
                    │
                    ▼
             ┌─────────────┐
             │   Analyze   │
             │   Question  │
             └──────┬──────┘
                    │
                    ▼
             ┌─────────────┐
             │   Retrieve  │
             │    Code     │
             └──────┬──────┘
                    │
                    ▼
             ┌─────────────┐
             │  Generate   │
             │   Answer    │
             └──────┬──────┘
                    │
                    ▼
                   END
```

That's enough for the MVP.

You don't need a complicated multi-agent architecture.

---

# LangGraph Nodes

## 1. `analyze_question`

Input:

```text
Where is authentication implemented?
```

The node determines what the user is asking about and prepares the query for retrieval.

For the MVP, this does not need sophisticated reasoning.

It can simply normalize the question and prepare a search query.

---

## 2. `retrieve_code`

The retrieval node searches the vector store.

Example:

```text
Question:
"Where is authentication implemented?"

Retrieved:

auth/routes.py
auth/service.py
auth/middleware.py
auth/models.py
```

The retrieved chunks are placed into the LangGraph state.

---

## 3. `generate_answer`

The LLM receives:

```text
User Question

+

Retrieved Code

+

Instructions
```

The prompt tells the LLM:

* Answer using the retrieved repository context.
* Do not invent implementation details.
* Mention relevant file paths.
* Explain the reasoning clearly.
* If the repository context is insufficient, say so.

Then the LLM generates the final answer.

---

# LangGraph State

The MVP state can be very small.

```text
State

question
   │
   ├── search_query
   │
   ├── retrieved_documents
   │
   └── answer
```

Conceptually:

```python
class AgentState(TypedDict):
    question: str
    search_query: str
    retrieved_documents: list
    answer: str
```

The state flows through the graph:

```text
question
   │
   ▼
analyze_question
   │
   ▼
search_query
   │
   ▼
retrieve_code
   │
   ▼
retrieved_documents
   │
   ▼
generate_answer
   │
   ▼
answer
```

---

# Why LangGraph?

A basic RAG pipeline could technically be written without LangGraph.

However, LangGraph gives the project an explicit workflow that can later be extended.

For example:

```text
              ┌──────────────┐
              │ Analyze      │
              │ Question     │
              └──────┬───────┘
                     │
                     ▼
              ┌──────────────┐
              │ Retrieve     │
              │ Code         │
              └──────┬───────┘
                     │
                     ▼
              ┌──────────────┐
              │ Generate     │
              │ Answer       │
              └──────┬───────┘
                     │
                     ▼
                    END
```

Later, you could add:

```text
Retrieve
   │
   ▼
Enough Context?
  / \
yes  no
 |    |
 ▼    ▼
Answer  Better Search
          │
          └──────► Retrieve
```

But this should **not** be part of the initial MVP unless the basic system works first.

---

# Example: Debugging a 401 Error

User asks:

> Why might this endpoint return 401?

The system retrieves relevant code:

```text
routes.py
auth.py
middleware.py
dependencies.py
```

The LLM can then explain the flow:

```text
1. Request reaches the endpoint.
2. Authentication dependency runs.
3. JWT token is extracted.
4. Token is validated.
5. Invalid/missing token raises HTTP 401.
6. Valid token allows the request to continue.
```

The important part is that the explanation should be grounded in the repository's actual code rather than generic knowledge.

---

# Example: Understanding a Login Flow

User:

> How does the login flow work?

Possible retrieval:

```text
routes.py
auth_service.py
user_repository.py
jwt.py
```

The answer could describe:

```text
Client
  │
  ▼
POST /login
  │
  ▼
Auth Route
  │
  ▼
Auth Service
  │
  ▼
User Repository
  │
  ▼
Password Verification
  │
  ▼
JWT Creation
  │
  ▼
Response
```

This is where the project becomes more useful than a simple "chat with PDF" RAG application.

---

# Technology Stack

## Backend

* Python
* FastAPI
* LangGraph
* LangChain
* LLM API
* Vector database
* GitHub API / Git
* Pydantic

## RAG

* Embedding model
* Vector store
* Code-aware chunking
* Metadata

## Frontend

The frontend will be added later.

Planned stack:

* React / Next.js
* TypeScript

The frontend is intentionally **not part of the first MVP implementation**.

---

# MVP User Flow

```text
Developer
    │
    ▼
Enter GitHub Repository
    │
    ▼
Repository Ingestion
    │
    ▼
Code Indexed
    │
    ▼
Chat Interface
    │
    ▼
Ask Question
    │
    ▼
LangGraph
    │
    ▼
RAG Retrieval
    │
    ▼
LLM
    │
    ▼
Answer
```

---

# Project Goals

The MVP should demonstrate that the system can:

* Understand a repository's source code.
* Retrieve relevant files/chunks.
* Answer natural-language questions.
* Explain code flows.
* Reference relevant file paths.
* Avoid hallucinating when context is insufficient.

---

# What This MVP Does NOT Include

To keep the project manageable, the first version will NOT include:

* Multiple specialized agents
* Autonomous coding
* Pull-request generation
* Automatic code modification
* Complex dependency analysis
* Full AST-based repository analysis
* Code execution
* CI/CD integration
* GitHub OAuth
* Multi-user authentication
* Persistent user accounts
* Advanced reranking
* Hybrid search
* Redis
* PostgreSQL
* Kubernetes
* Microservices
* Complex evaluation pipelines

These can be added later only if the MVP exposes a real need for them.

---

# Future Improvements

Once the MVP works, the system can evolve into:

```text
Basic RAG
    │
    ├── Better code chunking
    │
    ├── Hybrid search
    │
    ├── Dependency-aware retrieval
    │
    ├── Repository structure understanding
    │
    ├── Query routing
    │
    ├── Retrieval validation
    │
    ├── Conversation memory
    │
    ├── GitHub PR analysis
    │
    └── React / Next.js UI
```

The important rule is:

> Build the simple retrieval → reasoning → answer loop first. Add complexity only when the simple system fails on real repository questions.

---

# Core Architecture

```text
                GitHub
                   │
                   ▼
             Repository
              Ingestion
                   │
                   ▼
              Code Chunks
                   │
                   ▼
              Embeddings
                   │
                   ▼
             Vector Store
                   │
                   │
User Question ────┤
                   ▼
              LangGraph
                   │
          ┌────────┴────────┐
          ▼                 ▼
     Query Analysis      Retrieval
          │                 │
          └────────┬────────┘
                   ▼
             Retrieved Code
                   │
                   ▼
                  LLM
                   │
                   ▼
              Final Answer
```

---

# Final MVP Definition

The project is successful when a developer can give it a real GitHub repository and ask:

> "How does authentication work?"

and receive a useful answer grounded in the repository, including relevant files.

Then they can ask:

> "Why does `/api/users` return 401?"

and the system can retrieve the authentication-related code and explain the likely cause based on that code.

That is the core product.

Everything else comes later.
