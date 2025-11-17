# 💻 Frontend — Ecommerce AI Agent

This is the **Next.js 16 frontend** for the Ecommerce AI Agent project.  
It provides a modern, responsive interface for interacting with the AI-powered recommendation system.

---

## ⚙️ Tech Stack

- **Next.js 16** (React 19)
- **TypeScript**
- **TailwindCSS 4**
- **React Compiler (experimental)**
- **ESLint 9** for linting and code quality

---

## 🧠 Design Overview

- Built using the **App Router** architecture (`src/app/`).
- Uses **server components** for performance and scalability.
- Communicates with the **FastAPI backend** via REST API calls.
- Designed for **AI-driven product discovery** — users can input text or upload images to get recommendations.

---

## 🧩 Directory Structure

```
frontend/
├── public/           # Static assets
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── globals.css
│   └── styles/       # Tailwind and global styles
├── package.json
├── next.config.ts
└── tsconfig.json
```

---

## 🧰 Setup Instructions

### 1. Install dependencies
```bash
npm install
```

### 2. Run the development server
```bash
npm run dev
```

### 3. Build for production
```bash
npm run build
npm start
```

### 4. Access the app
- Local: http://localhost:3000

---

## 🔗 API Integration

The frontend communicates with the backend via:
```
POST http://localhost:8000/chat
```

Form fields:
- `query`: text input
- `image`: optional image file

---

## 🧪 Linting and Formatting

Run ESLint:
```bash
npm run lint
```

---

## 🧑‍💻 Author
**Collin Shen**  
AI Engineer & Full-Stack Developer  
