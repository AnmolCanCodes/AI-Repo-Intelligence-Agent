from typing import Dict, Any
from langchain_core.messages import SystemMessage, HumanMessage
from app.graph.state import AgentState
from app.retrieval.vectorstore import load_vectorstore
from app.retrieval.retriever import retrieve_relevant_chunks
from app.llm.client import create_llm
from app.llm.prompts import get_rag_prompt_template


def analyze_question(state: AgentState) -> Dict[str, Any]:
    """Transforms contextual follow-up questions into standalone vector search queries."""
    question = state["question"]
    chat_history = state.get("chat_history", [])

    # If there is no chat history, the question is already standalone
    if not chat_history:
        return {"search_query": question.strip()}

    # Prompt the LLM to resolve references like "it", "that file", "the second endpoint"
    llm = create_llm()
    
    # Format chat history into a readable string
    history_str = "\n".join([
        f"{'User' if msg.type == 'human' else 'Assistant'}: {msg.content}"
        for msg in chat_history[-6:]  # Keep last 3 turns for context
    ])

    reformulate_prompt = (
        "Given the conversation history and a follow-up question, rewrite the follow-up question "
        "to be a standalone search query that contains all necessary code context for vector retrieval.\n"
        "Do NOT answer the question, only return the rewritten search query.\n\n"
        f"Conversation History:\n{history_str}\n\n"
        f"Follow-up Question: {question}\n\n"
        "Standalone Search Query:"
    )

    response = llm.invoke([HumanMessage(content=reformulate_prompt)])
    standalone_query = response.content.strip()

    print(f"[Query Reformulation] Original: '{question}' -> Standalone: '{standalone_query}'")
    return {"search_query": standalone_query}


def retrieve_code(state: AgentState) -> Dict[str, Any]:
    """Retrieves top-k code chunks from vectorstore using the reformulated search query."""
    search_query = state["search_query"]
    vectorstore = load_vectorstore()
    docs = retrieve_relevant_chunks(vectorstore, query=search_query, k=5)
    return {"retrieved_documents": docs}


def generate_answer(state: AgentState) -> Dict[str, Any]:
    """Generates an answer using retrieved context and previous chat history."""
    question = state["question"]
    docs = state.get("retrieved_documents", [])
    chat_history = state.get("chat_history", [])

    if not docs:
        return {
            "answer": "The repository context does not provide enough information to answer this question."
        }

    # Format code chunks
    context_blocks = []
    for doc in docs:
        file_path = doc.metadata.get("file_path", "Unknown File")
        context_blocks.append(f"--- File: {file_path} ---\n{doc.page_content}")
    
    context_str = "\n\n".join(context_blocks)

    # Combine historical context + current question
    llm = create_llm()
    prompt_template = get_rag_prompt_template()

    # Pass chat history alongside current context
    chain = prompt_template | llm
    response = chain.invoke({
        "question": question,
        "context": context_str,
        "chat_history": chat_history  # Pass to prompt template
    })

    return {"answer": response.content}