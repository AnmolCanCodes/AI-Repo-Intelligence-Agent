from typing import TypedDict ,List
from langchain_core.documents import Document

class AgentState(TypedDict):
    question:str
    search_query:str
    retrieved_documents: List[Document]
    answer:str