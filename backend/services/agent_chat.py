from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver


# Use your own key here
# import os
# os.environ["OPENAI_API_KEY"] = "sk-your-key-here"


# 1. Define your state schema
class AgentState(TypedDict):
    query: str
    response: str

# 2. Initialize model
llm = ChatOpenAI(model="gpt-4o-mini")

# 3. Define node logic
def agent_node(state: AgentState):
    query = state["query"]
    response = llm.invoke(query)
    return {"response": response.content}

# 4. Build graph
graph = StateGraph(AgentState)
graph.add_node("agent", agent_node)
graph.set_entry_point("agent")
graph.add_edge("agent", END)

# Create the LangGraph app
memory = MemorySaver()
agent_app = graph.compile(checkpointer=memory)

# 5. Compile the app
app = graph.compile()

def chat(query: str):
    result = app.invoke({"query": query})
    print("AI:", result["response"])
    return {"response": result["response"]}

# 6. Run example
if __name__ == "__main__":
    user_query = input("User: ")
    result = app.invoke({"query": user_query})
    print("AI:", result["response"])
