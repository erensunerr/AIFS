
import base64
from openai import OpenAI
from dotenv import load_dotenv
import logging
from prompts import get_prompt

# Configure logging
logging.basicConfig(
    # level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

load_dotenv()

client = OpenAI()

def describe_image(image_path: str, context_dump : str = "") -> str:
    logger.info(f"Describing image: {image_path} with context: {context_dump}.")
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": get_prompt("describe_image")},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
                ]
            }
        ]
    )

    logger.info(f"Image description: {response.choices[0].message.content.strip()}")

    return response.choices[0].message.content.strip()
