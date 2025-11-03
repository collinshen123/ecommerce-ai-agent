from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services.agent import agent

class ChatRequest(BaseModel):
    query: str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "AI Commerce Agent is running."}

@app.post("/chat")
async def chat_with_agent(payload: ChatRequest):
    messages = [{"role": "user", "content": payload.query}]
    response = agent.invoke({"messages": messages})

    # Get all messages
    all_messages = response["messages"]

    # Find the last AIMessage that has actual content (not tool calls only)
    final_content = ""
    for msg in reversed(all_messages):
        if msg.type == "ai" and msg.content:  # Has text content
            final_content = msg.content
            break

    return {"response": final_content}
