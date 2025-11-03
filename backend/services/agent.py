from langchain.agents import create_agent
from .text_recommend import search_product
from .image_recommend import image_search


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
