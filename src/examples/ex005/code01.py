from langchain.chat_models import init_chat_model
from langchain.messages import SystemMessage
from langchain_core.messages import BaseMessage
from langchain_core.tools import tool

# criar as ferramentas


@tool
def multiply(a: float, b: float) -> float:
    """Multiply a * b and returns the result

    Args:
        a: float multiplicand
        b: float multiplier

    Returns:
        the resulting float of the equation a * b
    """
    return a * b


llm = init_chat_model("google_genai:gemini-2.0-flash")


system_message = SystemMessage(
    "You are a helpful assistent. You have accses to tools. When user asks for somiting, first look if you have a tool that solves that problem"
)
human_message = SystemMessage("Oi, me chamo Alexandre")
messages: list[BaseMessage] = [system_message, human_message]

result = llm.invoke(messages)
