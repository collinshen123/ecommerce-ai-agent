# 🛍️ Ecommerce AI Agent

An AI-powered e-commerce assistant that provides intelligent product recommendations using both **text** and **image** inputs.  
This project combines a **FastAPI backend** for AI logic and a **Next.js frontend** for a modern, responsive user interface.

---

## 🚀 Tech Stack

### Frontend
- **Next.js 16** (React 19)
- **TypeScript**
- **TailwindCSS 4**
- **React Compiler (experimental)**

### Backend
- **FastAPI**
- **LangChain / LangGraph**
- **ChromaDB** for vector storage
- **Sentence Transformers** for embeddings
- **OpenAI API** for LLM-based reasoning

---

## 🧠 Design Overview

- The **frontend** provides a clean interface for users to query the AI agent with text or upload an image.
- The **backend** handles:
  - Text and image embeddings
  - Product similarity search
  - AI-driven recommendations
- The two layers communicate via REST endpoints (`/chat`).

---

## 🧩 Project Structure

```
Ecommerce_AI_Agent/
├── backend/        # FastAPI backend
├── frontend/       # Next.js frontend
└── README.md       # Full project documentation
```

---

## 🧰 Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/Ecommerce_AI_Agent.git
cd Ecommerce_AI_Agent
```

### 2. Run the backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### 3. Run the frontend
```bash
cd ../frontend
npm install
npm run dev
```

### 4. Access the app
- Frontend: http://localhost:3000  
- Backend: http://localhost:8000

---

## 🐳 Docker Deployment

To run both frontend and backend together:
```bash
docker build -t ecommerce-ai-agent .
docker run -p 3000:3000 -p 8000:8000 ecommerce-ai-agent
```

---

## 🧑‍💻 Author
**Collin Shen**  
AI Engineer & Full-Stack Developer  