import os

# Copyright (c) 2025 Alexandre Toscano Diniz
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage
from rich import print

llm = init_chat_model(os.getenv("LLM_MODEL", "ollama:llama3.2"))

# mensagem que a ia vai receber como um prompt
system_message = SystemMessage("")

response = llm.invoke("Fale um pouco sobre você,como funciona e como pode ajudar.")

print(response)
