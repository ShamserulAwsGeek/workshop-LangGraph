import os
from typing import TyedDict, List, Union
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv  # used to store secret stuffs like API keys or configuration values.


load_dotenv()  # Load environment variables from a .env file

class AgentState(TypedDict):
    messages: List[Union[HumanMessage, AIMessage]]

llm= chatOpenAI(model = "gpt-4o")

def process(state:AgentState) -> AgentState:
    """this node will solve the requested input"""
    response = llm.invoke(state["messages"])

    state["messages"].append(AIMessage(content=response.content))
    print(f"nAI: {response.content}")
    print("CURRENT STATE:", state["messages"])
    return state

graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)
agent= graph.compile()

conversation_history = []

user_input = input("Enter: ")
while user_input != "exit":
    conversation_history.append(HumanMessage(content=user_input))
    result= agent.invoke({"messages":conversation_history})
    conversation_history = result["messages"]
    user_input = input("Enter: ")


with open("logging.txt", "w") as file:
    file.write("Your conversation Log:\n")

    for message in conversation_history:
        if isinstance(message, HumanMessage):
            file.write(f"You: {message.content}\n")

        elif isinstance(message, AIMessage):    
            file.write(f"AI: {message.content}\n")
        file.write("End of conversation.\n")

print("Conversation logged to logging.txt")
        