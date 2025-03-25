from langchain_core.tools import tool
from pydantic import BaseModel

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.tools import tool
from dotenv import load_dotenv
from langchain_core.messages import ToolMessage, AIMessage, HumanMessage
import logging

load_dotenv()

VECTOR_DIR = "data/clothing_vectors"

class DisplayItemInput(BaseModel):
    clothing_id: str
    title: str

@tool
def display_item_tool(items: list[DisplayItemInput]) -> None:
    """
    Instructs the UI to display a clothing item. Item must have:
        - clothing_id
        - title
    Example:
        display_item([{"clothing_id": "123", "title": "Beautiful Dress"}, {"clothing_id": "456", "title": "Stylish Jacket"}])
    """
    logging.info(f"Displaying {len(items)} clothing items")
    for item in items:
        logging.info(f"Item ID: {item.clothing_id}, Title: {item.title}")
    return None

def extract_display_items(messages):
    for msg in reversed(messages):
        # Check if it's a dict or LangChain message object

        if isinstance(msg, HumanMessage):
            break

        tool_calls = []
        if isinstance(msg, dict):
            tool_calls = msg.get("tool_calls", [])
        elif hasattr(msg, "tool_calls"):
            tool_calls = msg.tool_calls or []

        for call in tool_calls:
            name = call.get("name") if isinstance(call, dict) else getattr(call, "name", None)
            args = call.get("args") if isinstance(call, dict) else getattr(call, "args", {})

            if name == "display_item_tool":
                items = args.get("items", [])
                return [
                    {
                        "clothing_id": item["clothing_id"],
                        "title": item["title"],
                        "img_path": f"data/images/{item['clothing_id']}.jpg"
                    }
                    for item in items
                ]

    return []
