from typing import Annotated, Sequence, TypedDict
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage # The foundational class for all message types in LangGraph
from langchain_core.messages import ToolMessage # Passes data back to LLM after it calls a tool such as the content and the tool_call_id
from langchain_core.messages import SystemMessage # Message for providing instructions to the LLM
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool 
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

load_dotenv()

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


@tool
def add(a:int, b: int):
    """addition function to add two numbers"""
    return a + b

@tool
def subtract(a:int, b: int):
    """subtraction function to subtract two numbers"""
    return a - b

@tool
def multiply(a:int, b: int):
    """multiplication function to multiply two numbers"""
    return a * b

tools = [add, subtract, multiply]

model = chatOpenAI(model = "gpt-4o").blind_tools(tools)


def model_call(state: AgentState) -> AgentState:
    system_prompt = SystemMessage( content = "You are my AI assitant, please answer my query to the best of your ability")
    response = model.invoke([system_prompt] + state["messages"])
    return{"messages": [response]}

def should_continue(state:AgentState):
    messages = state["messages"]
    last_message = messages[-1]
    if not last_message.tool_calls:
        return "end"
    else: 
        return "continue"
    

graph =StateGraph(AgentState)
graph.add_node("our_agent", model_call)

tool_node = ToolNode(tools = tools)
graph.add_node("tool_node", tool_node)

graph.set_entry_point("our_agent")

graph.add_conditional_edges(
    "our_agent",
    should_continue,
    {
        "continue": "tools",
        "end": END,
    },

)

graph.add_edge("tools", "our_agent")
app = graph.compile()


def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()
        

inputs = {"messages":[{("user", "add 40 + 16  and then multiply the result by 4. also tell me a joke please")}]}
print_stream(app.stream(inputs, stream_mode = "values"))