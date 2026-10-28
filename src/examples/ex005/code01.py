import os
from xml.dom import ValidationErr

from langchain.chat_models import init_chat_model
from langchain.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain.tools import BaseTool
from langchain_core.messages import BaseMessage
from langchain_core.tools import tool

# Criar as ferramentas


@tool
def multiply(a: float, b: float) -> float:
    """Multiply a * b and returns the result.

    Args:
        a: float multiplicand
        b: float multiplier

    Returns:
        The resulting float of the equation a * b.
    """
    return a * b


# Inicializar o modelo

llm = init_chat_model(os.getenv("LLM_MODEL", "ollama:llama3.2"))


# Definir as mensagens

system_message = SystemMessage(
    "You are a helpful assistant. You have access to tools. "
    "When the user asks for something, first check whether "
    "you have a tool that can solve the problem."
)

human_message = HumanMessage("Oi, me chamo Alexandre. Me diga quanto é 1.13 vezes 3.21")

messages: list[BaseMessage] = [
    system_message,
    human_message,
]

# Lista de ferramentas
tools: list[BaseTool] = [multiply]
tools_by_name = {tool.name: tool for tool in tools}
llm_with_tools = llm.bind_tools(tools)


result = llm_with_tools.invoke(messages)
messages.append(result)

# Se existir uma lista de chamadas para minha ferramenta
if isinstance(result, AIMessage) and getattr(result, "tool_calls", None):
    call = result.tool_calls[-1]
    name, args, id_ = call["name"], call["args"], call["id"]

    status = "success"
    try:
        content = tools_by_name[name].invoke(args)
    except (KeyError, IndexError, TypeError, ValidationErr, ValueError) as error:
        content = f"Please,fix your mistakes: {error}"
        status = "error"

    tool_message = ToolMessage(content=content, tool_call_id=id_, status=status)

    messages.append(tool_message)

    result = llm_with_tools.invoke(messages)

    messages.append(result)

print(messages)
