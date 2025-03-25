from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()

VECTOR_DIR = "data/clothing_vectors"

def search_clothing(description: str, k: int = 3):
    print("Searching clothing...")
    embedding = OpenAIEmbeddings()
    vector_store = Chroma(
        persist_directory=VECTOR_DIR,
        embedding_function=embedding
    )

    # Search the vector store
    results = vector_store.similarity_search(description, k=k)

    # Extract and return clothing_ids in order
    return results

@tool
def search_clothing_tool(description: str) -> str:
    """
    Search the clothing vector store using a natural language description.
    Returns a text summary of top matches for the agent to mention or describe.
    """
    results = search_clothing(description, k=3)

    if not results:
        return "Sorry, I couldn't find any clothing that matches that description."

    return "\n\n".join([
        f"clothing_id: {doc.metadata['clothing_id']}\nDescription: {doc.page_content}"
        for doc in results
    ])
