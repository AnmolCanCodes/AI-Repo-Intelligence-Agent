from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

SYSTEM_PROMPT = """You are an expert AI codebase assistant. Your task is to explain and answer questions about a repository using ONLY the provided repository context.

Rules:
1. Ground your answer strictly in the provided context.
2. Always mention relevant file paths when explaining concepts.
3. Do NOT invent code, endpoints, or implementation details.
4. If the provided context is insufficient to answer the question, state clearly: "The repository context does not provide enough information to answer this question."
"""

USER_PROMPT_TEMPLATE = """Question:
{question}

Repository Context:
{context}
"""

def get_rag_prompt_template() -> ChatPromptTemplate:
    """Returns a structured ChatPromptTemplate for RAG generation."""
    return ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", USER_PROMPT_TEMPLATE)
    ])