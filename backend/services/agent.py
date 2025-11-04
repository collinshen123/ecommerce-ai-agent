from langchain.agents import create_agent
from .text_recommend import search_product
from .image_recommend import image_search
from fastapi import UploadFile
from langchain_core.messages import HumanMessage
import base64

SYSTEM_PROMPT = """
You are an AI assistant called Rufus. Only provide responses about the Amazon Storefront.
Do not answer questions outside of these topics.
Keep answers concise and informative.
Provide direct links when possible.
You have access to the `search_product` and `image_search` tools.
"""

agent = create_agent(
    model="gpt-4o-mini",
    tools=[search_product, image_search],
    system_prompt=SYSTEM_PROMPT
)


def run_agent(query: str, image: UploadFile | None = None):
    """
    Wrapper to handle multimodal input for the agent.
    If image is provided, attach it properly as base64 for vision-capable models.
    """
    content = []
    if query:
        content.append({"type": "text", "text": query})

    if image is not None:
        image_bytes = image.file.read()
        encoded = base64.b64encode(image_bytes).decode("utf-8")
        image.file.seek(0)
        content.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{encoded}"}
        })

    messages = [HumanMessage(content=content)]
    response = agent.invoke({"messages": messages})
    return response
