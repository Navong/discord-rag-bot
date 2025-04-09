# utils.py
from langchain_community.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
import pdfplumber
from dotenv import load_dotenv
import os
from langchain_chroma import Chroma



load_dotenv(override=True)
os.environ['OPENAI_API_KEY']
os.environ['GROQ_API_KEY']
db_name = "./chroma_db"

# Setup vector store and embeddings
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
# vector_store = InMemoryVectorStore(embeddings)


if os.path.exists(db_name):
    Chroma(persist_directory=db_name, embedding_function=embeddings).delete_collection()

# Create vectorstore
vector_store = Chroma(
    collection_name="my_collection",
    embedding_function=embeddings,
    persist_directory=db_name,  # Where to save data locally, remove if not necessary
)



async def update_index(file_path="./pdf/latest.pdf"):
    try:

        # Extract text from PDF
        with pdfplumber.open(file_path) as pdf:
            text = "".join(page.extract_text() for page in pdf.pages if page.extract_text())

        if not text:
            return None

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

        # Split text into chunks
        all_splits = text_splitter.split_text(text)

        # Add chunks to vector store
        docs = [Document(page_content=chunk) for chunk in all_splits]
        vector_store.add_documents(documents=docs, ids='doc1')


        return [len(docs)]
    except Exception as e:
        print(f"[update_index error]: {e}")
        return None

def reset_index():
    """
    Resets the Chroma vector store by deleting the 'my_collection' collection only.
    Keeps the database directory intact.
    """
    global vector_store

    try:
        # Create a Chroma client without a specific collection
        # client = Chroma(persist_directory=db_name, embedding_function=embeddings)
        vector_store.delete(ids=["doc1"])

        # Delete the collection by name
        # client.delete_collection("my_collection")
        print("Deleted collection: my_collection")
    except Exception as e:
        print(f"[reset_index error] Failed to delete collection: {e}")

    try:
        # Recreate the collection
        vector_store = Chroma(
            collection_name="my_collection",
            embedding_function=embeddings,
            persist_directory=db_name
        )
        print("Recreated vector store with collection: my_collection")
    except Exception as e:
        print(f"[reset_index error] Failed to recreate vector store: {e}")

@tool(response_format="content_and_artifact")
def retrieve_tool(query: str):
    """Retrieve information from the vector store."""
    retrieved_docs = vector_store.similarity_search(query, k=5)
    serialized = "\n\n".join(f"Content: {doc.page_content}" for doc in retrieved_docs)
    return serialized, retrieved_docs


# Set up LLM and ReAct Agent
llm = init_chat_model("gpt-4o-mini", model_provider="openai")
# llm = init_chat_model("llama-3.3-70b-versatile", model_provider="groq")
memory = MemorySaver()
agent_executor = create_react_agent(llm, [retrieve_tool], checkpointer=memory)