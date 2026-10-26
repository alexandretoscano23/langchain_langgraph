from langchain.chat_models import init_chat_model
from rich import print

# Atualizado para o modelo recomendado pela API do Google
llm = init_chat_model("google_genai:gemini-3.8-flash")

response = llm.invoke("Olá, tudo bem?")

print(response)
