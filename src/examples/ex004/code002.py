import os
import threading
from collections.abc import Sequence
from typing import Annotated, TypedDict

from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage
from langchain_core.messages import BaseMessage
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph, add_messages
from rich import print
from rich.markdown import Markdown

# modelo utilizado
llm = init_chat_model(os.getenv("LLM_MODEL", "ollama:llama3.2"))


# dados que passam de um nó para outro
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


# Definir o node
def call_llm(state: AgentState) -> AgentState:
    llm_result = llm.invoke(state["messages"])
    return {"messages": [llm_result]}


# criar o stategraph
builder = StateGraph(
    AgentState, context_schema=None, input_schema=AgentState, output_schema=AgentState
)


# Adicionar nodes ao grafo
builder.add_node("call_llm", call_llm)
builder.add_edge(START, "call_llm")
builder.add_edge("call_llm", END)


# Compilar o grafo
chackpointer = InMemorySaver()
graph = builder.compile()
config = RunnableConfig(configurable={"thread_id": threading.get_ident()})

if __name__ == "__main__":
    current_messages: Sequence[BaseMessage] = []
    while True:
        user_input = input("digite sua mensagem:")

        if user_input.lower() in ["q", "quit"]:
            print("Bye")
            print(Markdown("---"))
            break

        human_message = HumanMessage(user_input)
        result = graph.invoke({"messages": [human_message]}, config)

        print(Markdown(str(result["messages"][-1].content)))
        print(Markdown("---"))
