
# 🌟 **RAG & Chatbot Playground — LangChain • Groq • Open-Source LLMs**

An interactive collection of Retrieval-Augmented Generation pipelines, chatbots, vector search engines, and LLM applications built with **LangChain**, **FAISS**, **FastAPI**, and **Streamlit**.

Supports local & API-based LLMs like **Mistral**, **Gemma**, **Phi**, **DeepSeek**, and more.
Fetches knowledge from **PDFs, text files, websites, and structured/unstructured data sources**.

---

## 🚀 **Features**

* **RAG (Retrieval-Augmented Generation)** with FAISS, HuggingFace, and LangChain
* **Multi-model support:** Groq, OpenAI-compatible APIs, Mistral, DeepSeek, Gemma, Phi, Llama
* **Document ingestion:** PDF, TXT, Web Scraping, Wikipedia, ArXiv, HTML, custom text
* **Embeddings:** Sentence Transformers, LangChain embeddings
* **Vector Databases:** FAISS CPU
* **Interactive frontends:** Streamlit UI + FastAPI backend via LangServe
* **Environment file support:** `.env` for API keys (ignored by Git)
* **BeautifulSoup-based web scraping**
* **Chat history, memory components, and tools integrations**
* **Fully modular pipeline for training, retrieval & inference**

---

## 📁 **Project Structure (Example)**

```
📦 rag-chatbot-project
 ┣ 📜 app.py                # Streamlit UI
 ┣ 📜 server.py             # FastAPI / LangServe backend
 ┣ 📜 rag_pipeline.py       # Core RAG pipeline
 ┣ 📜 ingest.py             # PDF / TXT / Web ingestion
 ┣ 📜 vectorstore.py        # FAISS index builder
 ┣ 📜 models.py             # Model loaders (Groq, HF, OpenAI)
 ┣ 📜 utils.py              # Helpers
 ┣ 📜 requirements.txt
 ┣ 📜 .gitignore
 ┗ 📜 README.md
```

---

## 🧠 **LLM Support**

This repo supports:

### 🔥 **Open-Source Local Models**

* **Mistral**
* **Gemma**
* **Phi / Phi-2 / Phi-3**
* **DeepSeek**
* **Llama 2 / 3**
* **Mixtral**
* **Other HF models via `transformers` or `sentence-transformers`**

### ⚡ **API-Based Models**

* **Groq API** (blazing fast Llama/Gemma)
* **OpenAI-compatible models** (via LangChain)
* **LangChainHub hosted prompts**

---

## 📚 **Document & Data Sources**

You can load knowledge from:

* 📝 **TXT files**
* 📄 **PDF documents** (via PyPDF)
* 🌐 **Web pages** (BeautifulSoup + Requests)
* 📘 **Wikipedia**
* 📕 **ArXiv papers**
* 🧵 Custom datasets
* 🗂️ Mixed formats (HTML, markdown, transcripts, notes)

Everything gets chunked → embedded → stored in FAISS → retrieved during chat.

---

## 🎮 **How to Run**

### 1️⃣ **Install dependencies**

```
pip install -r requirements.txt
```

### 2️⃣ **Create your `.env` file**

```
OPENAI_API_KEY=
GROQ_API_KEY=
HUGGINGFACEHUB_API_TOKEN=
```

(The `.env` is automatically git-ignored.)

### 3️⃣ **Ingest your data**

```
python ingest.py --path documents/my.pdf
```

### 4️⃣ **Start the API server**

```
uvicorn server:app --reload
```

### 5️⃣ **Launch the Streamlit frontend**

```
streamlit run app.py
```

---

## 🏗 **Tech Stack**

### 🔹 Core Libraries

* **LangChain**
* **LangChain OpenAI**
* **LangChain Groq**
* **LangChain Community**
* **LangChainHub**

### 🔹 Vector Search

* **FAISS CPU**

### 🔹 Backend

* **FastAPI**
* **LangServe**
* **Uvicorn**
* **SSE Starlette (streaming responses)**

### 🔹 Frontend

* **Streamlit**

### 🔹 Utilities

* **python-dotenv**
* **BeautifulSoup4 (bs4)**
* **PyPDF**
* **Sentence Transformers**
* **Cassio (optional, Cassandra integrations)**

---

## 📦 **requirements.txt**

Includes everything you provided:

```
langchain-openai
langchain-core
python-dotenv
streamlit
langchain-community
langserve
fastapi
uvicorn
sse_starlette
bs4
pypdf
faiss-cpu
wikipedia
beautifulsoup4
cassio
arxiv
langchainhub
langchain
groq
langchain-groq
sentence_transformers
```

---

## 🧪 **RAG Workflow Overview**

```
          ┌──────────────┐
          │  Documents    │  (PDF / TXT / Web / Wiki)
          └──────┬───────┘
                 ▼
        ┌──────────────────┐
        │ Chunk & Embed     │  (SentenceTransformers)
        └──────┬───────────┘
               ▼
        ┌──────────────────┐
        │  FAISS Index      │  (Vector DB)
        └──────┬───────────┘
               ▼
      ┌──────────────────────┐
      │ Retriever + LLM       │  (Groq / OpenAI / OSS models)
      └──────────────────────┘
```

---

## 🌈 **Planned Enhancements**

* Multi-source hybrid search (web + PDF + knowledge base)
* Chat memory with long-term vector persistence
* Agents with tools & browser search
* GPU-accelerated local inference with VLLM / Ollama
* Conversation analytics dashboard

---


---

#  **1. Project Banner (Markdown)**


<h1 align="center">🔮 RAG & Chatbot Playground</h1>
<h3 align="center">LangChain • Groq • FAISS • Streamlit • Open-Source LLMs</h3>

<p align="center">
  Build fast, smart, modular AI systems using RAG, vector search, and modern LLM APIs.
</p>

<p align="center">
  <img src="[https://img.shields.io/badge/LangChain-RAG-blue](https://img.shields.io/badge/LangChain-RAG-blue)" />
  <img src="[https://img.shields.io/badge/FAISS-VectorDB-green](https://img.shields.io/badge/FAISS-VectorDB-green)" />
  <img src="[https://img.shields.io/badge/Groq-LLMs-orange](https://img.shields.io/badge/Groq-LLMs-orange)" />
  <img src="[https://img.shields.io/badge/Streamlit-UI-red](https://img.shields.io/badge/Streamlit-UI-red)" />
  <img src="[https://img.shields.io/badge/OpenSource-Models-yellow](https://img.shields.io/badge/OpenSource-Models-yellow)" />
</p>

---
---



```md


---
# 🧠 **2. Architecture Diagram (Mermaid + ASCII)** 

## 🧬 System Architecture

### 📊 Mermaid Diagram
```mermaid
flowchart TD
    A[User Query] --> B[Retriever]
    B --> C[FAISS Vector Store]
    B --> D[Document Loaders<br/>(PDF, TXT, Web, Wiki, ArXiv)]
    D --> E[Text Splitter]
    E --> F[Embeddings<br/>(Sentence Transformers)]
    F --> C
    B --> G[LLM Model<br/>(Groq / Mistral / Gemma / Phi)]
    G --> H[Final Response]

### **ASCII Diagram (if viewer doesn’t support Mermaid)**

```
User Query
          |
      Retriever ----- Document Loaders (PDF/TXT/Web/Wiki)
          |                   |
          |               Text Splitter
          |                   |
FAISS Vector Store <--- Embeddings (Sentence Transformers)
          |
    LLM Model (Groq / Mistral / Gemma / Phi)
          |
    Final Response
```

---

# 🔐 **4. `.env.example` file**

Create this file in your repo root:

```

# API Keys

OPENAI_API_KEY=
GROQ_API_KEY=
HUGGINGFACEHUB_API_TOKEN=

# Optional

LANGCHAIN_API_KEY=
LANGCHAIN_PROJECT=

````

Your `.env` stays hidden (thanks to `.gitignore`).  
`.env.example` tells users what variables they need.

---

# ⚡ **5. QuickStart Section (Clean & Simple)**

Add this below “Installation”:

```md
## ⚡ QuickStart

```bash
git clone https://github.com/<username>/<repo>.git
cd <repo>

# 1. Install dependencies
pip install -r requirements.txt

# 2. Copy the example environment file
cp .env.example .env
# Add your API keys in .env

# 3. Ingest documents
python ingest.py --path data/my.pdf

# 4. Start API server
uvicorn server:app --reload

# 5. Launch Streamlit application
streamlit run app.py
````

````

---

# 🔥 **6. Optional Add-On: “Models You Can Use” Section**

```md
## 🤖 Supported Open-Source LLMs

| Model | Mode | Provider |
|-------|--------|----------|
| **Mistral-7B** | Local / API | HF / Replicate |
| **Gemma 2B/7B** | Local / API | Groq / HF |
| **Phi-2 / Phi-3** | Local | HF |
| **DeepSeek R1** | API | Deepseek |
| **Llama 3** | API / Local | Groq / HF |
````


## 🤝 **Contributing**

PRs are welcome!
This repo is built to be modular — add new ingestion methods, new models, or new RAG pipelines.

---

## 👑 **Author**

**Dhruv (xetsef)**
AI • RAG Systems • LLM Engineering
Crafting intelligent systems with a little spark ✨

