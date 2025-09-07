from dotenv import load_dotenv

load_dotenv()
from typing import Annotated

from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model

llm = init_chat_model(
    model="gpt-4.1-mini",
    model_provider="openai",
)


class State(TypedDict):
    messages: Annotated[list, add_messages]


def chat(state: State):
    response = llm.invoke(state.get("messages", []))
    return {"messages": response}


def sampleNode(state: State):
    return {"messages": state["messages"] + ["This is sample node"]}


grapgh_builder = StateGraph(State)
grapgh_builder.add_node("chat", chat)
grapgh_builder.add_node("sampleNode", sampleNode)

grapgh_builder.add_edge(START, "chat")
grapgh_builder.add_edge("chat", "sampleNode")
grapgh_builder.add_edge("sampleNode", END)

graph = grapgh_builder.compile()

updated_state = graph.invoke(State({"messages": ["Hi my name is John"]}))
print("updated_state:", updated_state)
