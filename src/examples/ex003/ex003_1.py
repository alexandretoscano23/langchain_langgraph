from typing import TypedDict, Annotated
from rich import print
from langgraph.graph import END, START, StateGraph, add_messages
import operator


# reducer - função que vai juntar a (resultado anterior) + b (o resultado que está gerando agora)
# def reducer(a: list[str], b: list[str]) -> list[str]:
#     return a + b


# Definir o meu estado
# com o Annotated,você diz ao langGraph como combinar o valor antigo com o novo (para não sobrescrever)
# add_messages é um reducer que faz mais checagens
class State(TypedDict):
    nodes_path: Annotated[list[str], add_messages]


# Definir os nodes
def node_a(state: State) -> State:
    output_state: State = {"nodes_path": ["A"]}
    print("> node_a", f"{state=}", f"{output_state}")
    return output_state


def node_b(state: State) -> State:
    output_state: State = {"nodes_path": ["B"]}
    print("> node_b", f"{state=}", f"{output_state}")
    return output_state


# Definir o builder do grafo
builder = StateGraph(State)

builder.add_node("A", node_a)  # nome do node e sua função

builder.add_node("B", node_b)

# conectar as edges
builder.add_edge(START, "A")

builder.add_edge("A", "B")

builder.add_edge("B", END)

# Compilar o grafo
graph = builder.compile()

# Pegar o resutado
response = graph.invoke({"nodes_path": []})

# Resultado de todo o grafo

print()
print(f"{response}")
print()
