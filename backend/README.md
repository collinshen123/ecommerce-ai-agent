# 🧠 Backend — Ecommerce AI Agent

This is the **FastAPI backend** for the Ecommerce AI Agent project.  
It powers the AI-driven recommendation system that processes both **text** and **image** queries to suggest relevant products.

---

## ⚙️ Tech Stack

- **FastAPI** — lightweight Python web framework  
- **ChromaDB** — vector database for semantic search  
- **Sentence Transformers** — for text and image embeddings  
- **LangChain / LangGraph** — for LLM orchestration  
- **OpenAI API** — for natural language reasoning  
- **Pandas** — for catalog data handling  

---

## 🧩 Architecture Overview

1. **`main.py`** — FastAPI entry point exposing `/chat` endpoint.  
2. **`services/`** — contains modular logic for:
   - `agent.py`: main AI reasoning agent  
   - `text_recommend.py`: text-based product recommendations  
   - `image_recommend.py`: image similarity search  
3. **`data/`** — contains product catalog and embeddings.

---

## 🧠 Design Choices

- **FastAPI** chosen for async performance and easy API definition.  
- **ChromaDB** used for efficient vector similarity search.  
- **Sentence Transformers** provide robust embeddings for both text and images.  
- **LangChain** integrates LLM reasoning for contextual recommendations.

---

## 🧰 Setup Instructions

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the backend
```bash
uvicorn main:app --reload
```

### 3. Access the API
- Base URL: `http://localhost:8000`
- Endpoint: `POST /chat`
  - **Form fields:**
    - `query`: text input
    - `image`: optional image file

---

## 📁 Directory Structure

```
backend/
├── main.py
├── requirements.txt
├── services/
│   ├── agent.py
│   ├── text_recommend.py
│   └── image_recommend.py
└── data/
    ├── amazon_catalog.csv
    ├── amazon_catalog_with_images.csv
    └── chroma_db/
```

---

## 🧑‍💻 Author
**Collin Shen**  
AI Engineer & Full-Stack Developer  
