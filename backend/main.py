from fastapi import FastAPI, File, UploadFile, Form
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
async def chat_with_agent(query: str = Form(...), image: UploadFile | None = File(None)):
    messages = [{"role": "user", "content": query}]

    # If an image is provided, trigger image_search directly
    if image:
        from services.image_recommend import image_search
        # The @tool decorator wraps the function, so retrieve the original callable
        result = image_search.func(image)
        # Return only a text-safe summary message for React rendering
        summary = "Here are similar products:\n"
        for item in result["results"]:
            if "message" in item:
                summary += f"- {item['message']}\n"
            else:
                summary += (
                    f"- {item.get('title', 'Unknown')} by {item.get('brand', 'Unknown')} "
                    f"(${item.get('price', 'N/A')}, Rating: {item.get('rating', 'N/A')})\n"
                )

        return {
            "response": summary.strip(),
            "query_file": result["query_file"],
            "type": result["type"]
        }

    # Otherwise, handle text-based query through the conversational agent
    response = agent.invoke({"messages": messages})

    # Extract the last AI message
    final_content = ""
    for msg in reversed(response["messages"]):
        if getattr(msg, "type", None) == "ai" and getattr(msg, "content", ""):
            final_content = msg.content
            break

    return {"response": final_content}
