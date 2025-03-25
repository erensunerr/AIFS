from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

from prompts import get_prompt

# # Import your tools
# from tools.search_clothing import search_clothing
# from tools.mention_clothing import mention_clothing
# from tools.link_clothing_description import link_clothing_description
# from tools.proactive import proactive
# from tools.describe_image import describe_image

load_dotenv()

llm = init_chat_model("gpt-4o-mini", model_provider="openai")

tools = [

]

memory = MemorySaver()

aifs_agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt=get_prompt("system_prompt"),
    checkpointer=memory
)

def run_agent(user_input: str):
    """Main entry point for sending user input to the AIFS agent."""
    config = {"configurable": {"thread_id": "test-thread"}}
    return aifs_agent.invoke(
        {
            "messages": [
                ("user", user_input)
            ]
        }, config)

def proactive(admin_prompt: str):
    """Send a proactive suggestion according to the admin prompt."""
    config = {"configurable": {"thread_id": "test-thread"}}
    return aifs_agent.invoke(
        {
            "messages": [
                ("admin", admin_prompt)
            ]
        }, config)
