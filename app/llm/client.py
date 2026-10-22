from app.config.settings import settings


def create_llm():
    """Initializes and returns an LLM instance using OpenRouter."""
    token = settings.openrouter_api_key_str
    model_name = settings.openrouter_model_name

    if not token:
        raise ValueError(
            "OPENROUTER_API_KEY is not set. Add it to your environment or .env file before using the chat endpoint."
        )

    if not model_name:
        raise ValueError(
            "OPENROUTER_MODEL is not set. Add it to your environment or .env file before using the chat endpoint."
        )

    try:
        from langchain_openai import ChatOpenAI
    except ImportError as exc:
        raise RuntimeError(
            "OpenRouter support requires the 'langchain-openai' package. Install it in your Python environment before using the chat endpoint."
        ) from exc

    return ChatOpenAI(
        model=model_name,
        api_key=token,
        base_url="https://openrouter.ai/api/v1",
        temperature=0.1,
    )

