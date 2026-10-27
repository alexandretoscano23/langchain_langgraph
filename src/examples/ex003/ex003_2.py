import operator
from dataclasses import dataclass
from typing import Annotated, Literal

from langgraph.graph import END, START, StateGraph
from rich import print as rprint


@dataclass
class State:
    nodes_path: Annotated[list[str], operator.add]
    current_number: int = 0


def node_a(state: State) -> State:
    output_state = State(nodes_path=["A"], current_number=state.current_number)
    rprint("> node_a", f"{state=}", f"{output_state}")
    return output_state


def node_b(state: State) -> State:
    output_state = State(nodes_path=["B"], current_number=state.current_number)
    rprint("> node_b", f"{state=}", f"{output_state}")
    return output_state


def node_c(state: State) -> State:
    output_state = State(nodes_path=["C"], current_number=state.current_number)
    rprint("> node_c", f"{state=}", f"{output_state}")
    return output_state


limit_for_c = 50


def the_conditional(state: State) -> Literal["B", "C"]:
    if state.current_number >= limit_for_c:
        return "C"
    return "B"


builder = StateGraph(State)

builder.add_node("A", node_a)
builder.add_node("B", node_b)
builder.add_node("C", node_c)

builder.add_edge(START, "A")
builder.add_conditional_edges("A", the_conditional)
builder.add_edge("B", END)
builder.add_edge("C", END)

graph = builder.compile()

print(graph.get_graph().draw_mermaid())

print()
response = graph.invoke(State(nodes_path=[], current_number=51))
rprint(response)
