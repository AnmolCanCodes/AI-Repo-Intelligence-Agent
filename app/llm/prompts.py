from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

SYSTEM_PROMPT = """You are an expert AI codebase assistant. Answer questions about the repository using ONLY the provided code context.

Rules:
1. Ground your answers strictly in the provided context.
2. Always cite relevant file paths.
3. Do NOT invent code or details not present in the context.
4. If the context is insufficient, state that clearly.
"""

USER_PROMPT_TEMPLATE = """Repository Context:
{context}

Question: {question}"""


def get_rag_prompt_template() -> ChatPromptTemplate:
    """Returns a prompt template supporting multi-turn chat history."""
    return ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="chat_history"),  # Injects past messages dynamically
        ("human", USER_PROMPT_TEMPLATE)
    ])