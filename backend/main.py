from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services.agent import agent  # your agent from earlier

class ChatRequest(BaseModel):
    query: str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "AI Commerce Agent is running."}

@app.post("/chat")
async def chat_with_agent(payload: ChatRequest):
    # Build a message list for the agent as per LangChain format
    messages = [{"role": "user", "content": payload.query}]
    response = agent.invoke({"messages": messages})
    # If you want just the result text, extract it based on your agent's output schema
    if isinstance(response, dict) and "output" in response:
        return {"response": response["output"]}
    return {"response": response}
