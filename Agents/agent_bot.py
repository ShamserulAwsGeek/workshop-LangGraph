from typing import TypedDict, Lists
from langchian_core.messages import HumanMessage
from lanchchai_openai import chatOpenAI
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotend  #used to store secret stuffs like API keys or configuration values.

load_dotenv()  # Load environment variables from a .env file

class AgentState(TypedDict):
    messages: Lists[HumanMessage]

llm = chatOpenAI(model = "gpt-4o")


def process(state: AgentState) -> AgentState:
    response = llm.invoke(state["messages"])
    print(f"n\nAI: {response.content}")
    return state


graph = StateGraph(AgentState)
graph.add_node("process," process)
graph.add_edge(START, "process")
graph.add_edge("process", END )
agent = graph.compile()


user_input = input("Enter: ")
while user_input != "exit":
  agent.invoke({"messages": [HumanMessage(content=user_input)]})
  user_input = input("Enter: ")


