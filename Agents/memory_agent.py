import os
from typing import TyedDict, List, Union
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv  # used to store secret stuffs like API keys or configuration values.


load_dotenv()  # Load environment variables from a .env file

class AgentState(TypedDict):
    messages: List[Union[HumanMessage, AIMessage]]

llm= chatOpenAI(model = "gpt-40")

def process(state:AgentState) -> AgentState:
    """this node will solve the requested input"""
    response = llm.invoke(state["messages"])

    state["messages"].append(AIMessage(content=response.content))
    print(f"nAI: {response.content}")
    print("CURRENT STATE:", state["messages"])
    return state
