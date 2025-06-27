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

pdf_path = "Stock_Market_Performance_2024.pdf"

# Safety measure I have put for debugging purposes :)
if not os.path.exists(pdf_path):
    raise FileNotFoundError(f"PDF file not found: {pdf_path}")

pdf_loader = pyPDFLoader(pdf_path)  # This loads the PDF

# Checks if the PDF is there
try: 
    pages = pdf_loader.load()
    print(f"pdf has been loaded and has {len(pages)} pages")

except Exception as e:
    print(f"Error loading PDF: {e}")
    raise

#chunking process:
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,  # Size of each chunk
    chunk_overlap=200,  # Overlap between chunks
)

pages_split = text_splitter.split_documents(pages) # We now apply this to our pages
persist_directory = r"C:\mhaque\LangGraph_Book\LangGraphCourse\Agents"  # Directory to persist the database
collection_name = "rag_collection"  # Name of the collection


# If our collection does not exist in the directory, we create using the os command
if not os.path.exists(persist_directory):
    os.makedirs(persist_directory)


try:
    # Here, we actually create the chroma database using our embeddigns model
    vectorstore = chroma.from_documents(
        documents = pages_split,
        embedding = embeddings,
        persist_directory = persist_directory,
        collection_name = collection_name
    )
    print(f"Created ChromaDB vector store!")

except Exception as e:
    print(f"Error setting up ChromaDB: {e}")
    raise

# Now we create our retriever 
retriever = vectorstore.as_retriever(
    search_type = "similarity",  # Type of search to perform
    search_kwargs = {"k": 5 } # Number of documents to retrieve
)    