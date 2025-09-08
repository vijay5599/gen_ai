from dotenv import load_dotenv

load_dotenv()
from typing import Literal, Optional, Annotated
from openai import OpenAI
from typing_extensions import TypedDict
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.mongodb import MongoDBSaver
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


grapgh_builder = StateGraph(State)
grapgh_builder.add_node("chat", chat)

grapgh_builder.add_edge(START, "chat")
grapgh_builder.add_edge("chat", END)
graph = grapgh_builder.compile()


def compile_graph_with_checkpointer(checkpointer):
    return grapgh_builder.compile(checkpointer=checkpointer)


DB_URI = "mongodb://admin:admin@localhost:27017"
with MongoDBSaver.from_conn_string(DB_URI) as checkpointer:
    graph_with_checkpoint = compile_graph_with_checkpointer(checkpointer=checkpointer)
    config = {"configurable": {"thread_id": "Vijay"}}
    for chunk in graph_with_checkpoint.stream(
        State({"messages": ["can u give 2 line defination for langgraph"]}),
        config=config,
        stream_mode="values",
    ):
        chunk["messages"][-1].pretty_print()
