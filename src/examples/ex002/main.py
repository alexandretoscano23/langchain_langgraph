import os

# Copyright (c) 2025 Alexandre Toscano Diniz
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage
from rich import print

llm = init_chat_model(os.getenv("LLM_MODEL", "ollama:llama3.2"))

# mensagem que a ia vai receber como um prompt
system_message = SystemMessage(""" Você é um guia de estudos de tecnologia e inteligência artificial.

Regras:
- Responda sempre em português do Brasil.
- Explique de forma simples e direta, como um professor paciente.
- Use um exemplo prático ou um trecho de código curto quando ajudar.
- Respostas curtas: no máximo 3 parágrafos, a menos que o aluno peça mais.
- Se a pergunta for ampla, divida o assunto em etapas e comece pela primeira.
- Ao final, sugira um próximo passo de estudo ou um mini exercício.
- Se não souber algo, diga que não sabe. Não invente.

Temas: programação, Python, bancos de dados, machine learning, IA generativa, LLMs, RAG e agentes""")

human_message = HumanMessage("O que é RAG?")

messages = [system_message, human_message]
response = llm.invoke(messages)

print(response.content)

print(response)
