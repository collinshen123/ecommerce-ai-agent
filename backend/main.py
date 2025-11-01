from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from services import text_recommend, image_recommend
from services.agent_chat import chat
from pydantic import BaseModel


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

@app.post("/recommend")
async def recommend_products(query: str):
    return text_recommend.recommend_products(query)

@app.post("/image-search")
async def search_image(file: UploadFile):
    return image_recommend.search_by_image(file)

@app.post("/chat")
async def chat_with_agent(payload: ChatRequest):
    return chat(payload.query)
