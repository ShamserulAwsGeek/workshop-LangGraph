from dotenv import load_dotenv
import os
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, HumanMessage, ToolMessage, SystemMessage
from operator import add as add_messages
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import pyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.tools import tool

load_dotenv()

llm = ChatOpenAI(
    model = "gpt-4o", temperature= 0) # I want to minimize hallucination - temperature = 0 makes the model output more deterministic 


# Our Embedding Model - has to also be compatible with the LLM

embeddings = OpenAIEmbeddings(
    model = "text-embedding-3-small",
)