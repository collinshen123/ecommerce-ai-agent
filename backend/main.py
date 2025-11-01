from fastapi import FastAPI, UploadFile
from services import text_recommend, image_recommend, agent

app = FastAPI()

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
async def chat_with_agent(message: str):
    return agent.handle_chat(message)
