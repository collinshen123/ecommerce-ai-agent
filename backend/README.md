Backend Readme

run backend:
uvicorn main:app --reload



first used SentenceTransformerEmbeddingFunction("all-MiniLM-L6-v2") for text embeddings. just for text embedding.
Wanted to implement image search so changed to a more robust embedding model and changed the chromadb schema
