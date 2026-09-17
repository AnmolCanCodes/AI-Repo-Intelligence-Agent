from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

from app.config.settings import settings


def create_llm():
    """Initializes and returns the HuggingFace Chat LLM instance."""
    token = settings.hf_token_str
    if not token:
        raise ValueError(
            "HF_TOKEN is not set. Add it to your environment or .env file before using the chat endpoint."
        )

    llm = HuggingFaceEndpoint(
        repo_id=settings.HF_MODEL,
        task="text-generation",
        huggingfacehub_api_token=token,
        temperature=0.1,
        max_new_tokens=512,
    )

    return ChatHuggingFace(llm=llm)

