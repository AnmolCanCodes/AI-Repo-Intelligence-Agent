from typing import TypedDict, List
from langchain_core.documents import Document
from langchain_core.messages import BaseMessage


class AgentState(TypedDict):
    question: str
    chat_history: List[BaseMessage]  # Stores past messages: [HumanMessage, AIMessage, ...]
    search_query: str
    retrieved_documents: List[Document]
    answer: str