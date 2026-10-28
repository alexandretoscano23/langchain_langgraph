import os

from langchain.chat_models import BaseChatModel, init_chat_model


def load_llm() -> BaseChatModel:
    return init_chat_model(os.getenv("LLM_MODEL", "ollama:llama3.2"))
