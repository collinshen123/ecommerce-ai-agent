from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict, Literal, Annotated
import operator
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool
from .text_recommend import search_product


# Use your own key here
# import os
# os.environ["OPENAI_API_KEY"] = "sk-your-key-here"


# 1. Define your state schema
class AgentState(TypedDict):
    query: str
    response: str
    tool_calls: Annotated[list[dict], operator.add]

# 2. Initialize model
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
# Bind the tool *once* – the model will now output a `tool_call` when needed
llm_with_tools = llm.bind_tools([search_product])

# 3. Define node logic
SYSTEM_PROMPT = """
You are an AI assistant called Rufus. Only provide responses about the Amazon Storefront.
Do not answer questions outside of these topics.
Keep answers concise and informative.
Provide direct links when possible.
You have access to the `search_product` tool.
"""

def agent_node(state: AgentState):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": state["query"]},
    ]

    # If we already executed a tool, feed its result back
    if state.get("tool_calls"):
        # `tool_calls` contains the raw dicts from the model.
        # We turn the last tool result into a ToolMessage.
        last_tool_result = state["tool_calls"][-1]["result"]
        messages.append(ToolMessage(content=last_tool_result,
                                   tool_call_id=state["tool_calls"][-1]["id"]))

    response = llm_with_tools.invoke(messages)

    # Detect tool calls in the response
    tool_calls = []
    if response.tool_calls:
        for tc in response.tool_calls:
            tool_calls.append({
                "id": tc.id,
                "name": tc.name,
                "args": tc.args,
                "result": None   # will be filled by tool_node
            })

    return {
        "response": response.content if not tool_calls else "",
        "tool_calls": tool_calls
    }

def tool_node(state: AgentState):
    results = []
    for tc in state["tool_calls"]:
        if tc["result"] is not None:      # already executed
            continue

        # Find the Python function
        tool_func = {
            "search_product": search_product
        }[tc["name"]]

        # Call it
        raw_result = tool_func.invoke(tc["args"])
        results.append({
            **tc,
            "result": raw_result
        })

    # Replace the old list with the enriched one
    return {"tool_calls": results}

def should_continue(state: AgentState) -> Literal["tool", "END"]:
    if state.get("tool_calls") and any(tc["result"] is None for tc in state["tool_calls"]):
        return "tool"
    return END

# 4. Build graph
graph = StateGraph(AgentState)

graph.add_node("agent", agent_node)
graph.add_node("tool",  tool_node)

graph.set_entry_point("agent")
graph.add_conditional_edges("agent", should_continue, {"tool": "tool", "END": END})
graph.add_edge("tool", "agent")          # after tool → back to agent for final answer

# In your agent_chat.py or agent.py
memory = MemorySaver()
app = graph.compile(checkpointer=memory)

def chat(query: str, thread_id: str = "default_user"):
    result = app.invoke(
        {"query": query, "response": "", "tool_calls": []},
        config={"configurable": {"thread_id": thread_id}}
    )
    return result

# 6. Run example
if __name__ == "__main__":
    while True:
        user = input("\nUser: ")
        if user.lower() in {"quit", "exit"}:
            break
        chat(user)
