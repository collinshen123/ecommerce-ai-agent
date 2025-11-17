from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services.agent import run_agent

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
async def chat_with_agent(query: str = Form(...), image: UploadFile | None = File(None)):
    messages = [{"role": "user", "content": query}]

    # Let the agent decide which tool to invoke
    inputs = {"messages": messages}
    if image is not None:
        inputs["image"] = image
    response = run_agent(query, image)

    # Extract final AI message content
    final_content = ""
    for msg in reversed(response["messages"]):
        if getattr(msg, "type", None) == "ai" and getattr(msg, "content", ""):
            final_content = msg.content
            break

    return {"response": final_content}
