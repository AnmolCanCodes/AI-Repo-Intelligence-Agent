from typing import Dict, Any
from app.graph.state import AgentState
from app.retrieval.vectorstore import load_vectorstore
from app.retrieval.retriever import retrieve_relevant_chunks
from app.llm.client import create_llm
from app.llm.prompts import get_rag_prompt_template

def analyze_question(state:AgentState)-> Dict[str,Any]:
    """Normalizes and prepares the user;s question for retrieval"""

    question = state["question"]
    search_query = question.strip() #santize query fro vector srch
    return {'search_query': search_query}

def retrieve_code(state:AgentState)->Dict[str,Any]:
    """Retrieves top-k code chunks from the FAISS vector"""
    search_query = state["search_query"]

    vectorstore = load_vectorstore()

    docs = retrieve_relevant_chunks(vectorstore,query=search_query,k=5)

    return {"retrieved_documents": docs}

def generate_answer(state:AgentState)->Dict[str,Any]:
    """format retrieved code context and ivokes from the LLM to construct the answer"""

    question = state["question"]
    docs = state.get("retrieved_documents",[])

    if not docs:
        return{
        "answer": "The repository context does not provie enough information to answer this question"
        }

    context_blocks = []
    for doc in docs:
        file_path = doc.metadata.get("file_path", "Unknown File")
        context_blocks.append(f"--- File: {file_path} ---\n{doc.page_content}")
    
    context_str = "\n\n".join(context_blocks)

    # Initialize LLM and Prompt Template
    llm = create_llm()
    prompt = get_rag_prompt_template()

    # Create processing chain: prompt -> llm
    chain = prompt | llm

    # Generate response
    response = chain.invoke({
        "question": question,
        "context": context_str
    })

    return {"answer": response.content}
