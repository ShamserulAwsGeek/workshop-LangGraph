from typing import Annotated, Sequence, TypedDict
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

load_dotenv()

# This is the global variable to store document 
document_content = ""

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


@tool
def update(content: str) -> str:
    """update the document with the provided content"""
    global document_content
    document_content = content 
    return f"Document has been updated successfully! The current content is :\n{document_content}"

@tool
def save(filename: str) -> str:
    """ save the current document to a text file and finish the process.

    Args:
        filename: Name for the text file
    """
    global document_content 

    if not filename.endswith('.txt'):
        filename = f"{filename}.txt"

    try: 
        with open(filename, 'w') as file: 
            file.write(document_content)
        print(f"\n document has been saved to: {filename}")
        return f"Document has been saved to '{filename}' successfully!"
    except Exception as e:
        return f"Error saving document: {str(e)}"
    
    tools =[update, save]

    model = ChatOpenAI(model= "gpt-4o").bind_tools(tools)