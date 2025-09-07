from dotenv import load_dotenv

load_dotenv()
from typing import Literal, Optional
from openai import OpenAI
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model

llm = init_chat_model(
    model="gpt-4.1-mini",
    model_provider="openai",
)
client = OpenAI()


class State(TypedDict):
    user_query: str
    llm_output: Optional[str]
    is_good: Optional[bool]


def chat_bot(state: State):

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": state["user_query"]},
        ],
    )
    state["llm_output"] = response.choices[0].message.content
    return state


def gemini_chat_bot(state: State):

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": state["user_query"]},
        ],
    )
    state["llm_output"] = response.choices[0].message.content
    return state


def evaluate_response(state: State) -> Literal["gemini_chat_bot", "end_node"]:
    # A simple evaluation function that marks the response as good if it contains the word "good"
    if True:
        return "end_node"
    return "gemini_chat_bot"


def end_node(state: State):
    return state


graph_builder = StateGraph(State)
graph_builder.add_node("chat_bot", chat_bot)
graph_builder.add_node("gemini_chat_bot", gemini_chat_bot)
graph_builder.add_node("evaluate_response", evaluate_response)  # Decision node
graph_builder.add_node("end_node", end_node)

graph_builder.add_edge(START, "chat_bot")
graph_builder.add_conditional_edges("chat_bot", evaluate_response)
graph_builder.add_edge("gemini_chat_bot", "end_node")
graph_builder.add_edge("end_node", END)

graph = graph_builder.compile()

updated_state = graph.invoke(State({"user_query": "hey what is 2+2?"}))
print("updated_state:", updated_state)
