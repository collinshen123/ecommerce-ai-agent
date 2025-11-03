from fastapi import UploadFile
from PIL import Image
import io
import torch
from sentence_transformers import SentenceTransformer
import chromadb
from langchain_core.tools import tool

# Initialize the model and database client once
model = SentenceTransformer("clip-ViT-B-32")
client = chromadb.PersistentClient(path="./data/chroma_db")
collection = client.get_collection(name="amazon_products")

@tool
def image_search(file: UploadFile) -> dict:
    """
    Perform a visual similarity search for an uploaded image using CLIP embeddings.

    Args:
        file (UploadFile): An image uploaded via FastAPI endpoint or Agent Tool.

    Returns:
        dict: List of recommended products most visually similar to the uploaded image.
    """
    # Read and preprocess image
    image_bytes = file.file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    # Compute CLIP image embedding
    image_embedding = model.encode([image], convert_to_tensor=True, normalize_embeddings=True)
    image_embedding = image_embedding.cpu().numpy().tolist()

    # Query Chroma for nearest items (assumes unified collection)
    results = collection.query(
        query_embeddings=image_embedding,
        n_results=3,
        include=["metadatas", "distances"]
    )

    response_items = []
    if results["metadatas"][0]:
        for i, meta in enumerate(results["metadatas"][0]):
            dist = results["distances"][0][i]
            response_items.append({
                "title": meta.get("title"),
                "brand": meta.get("brand"),
                "category": meta.get("category"),
                "price": meta.get("price"),
                "image_url": meta.get("image_url", None),
                "rating": meta.get("rating"),
                "distance": dist
            })
    else:
        response_items.append({"message": "No similar products found."})

    # Ensure response is safe and easily serializable for frontend rendering
    safe_results = []
    for item in response_items:
        if "message" in item:
            safe_results.append(item)
        else:
            safe_results.append({
                "title": str(item.get("title", "")),
                "brand": str(item.get("brand", "")),
                "category": str(item.get("category", "")),
                "price": float(item.get("price", 0.0)) if item.get("price") else None,
                "image_url": str(item.get("image_url", "")),
                "rating": float(item.get("rating", 0.0)) if item.get("rating") else None,
                "distance": float(item.get("distance", 0.0))
            })

    return {
        "type": "image_search",
        "query_file": file.filename,
        "results": safe_results
    }