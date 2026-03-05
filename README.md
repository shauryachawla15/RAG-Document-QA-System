📄 Streamlit RAG Document Chatbot

A Retrieval-Augmented Generation (RAG) based document chatbot built using Streamlit, ChromaDB, and MiniLM embeddings.
Users can upload PDF or DOC/DOCX files and ask questions about the document through an interactive chat interface.

The system processes the document, stores embeddings in a vector database, retrieves relevant chunks, and generates answers based on the document context.

🚀 Features

✅ Upload PDF / DOC / DOCX documents
✅ Automatic text extraction and chunking
✅ MiniLM-L6-v2 embeddings for semantic search
✅ ChromaDB vector database for storage
✅ RAG pipeline for contextual answers
✅ Streamlit chat interface
✅ Ask questions directly related to uploaded documents

🧠 Architecture
User Uploads Document
        │
        ▼
Document Loader (PDF/DOCX)
        │
        ▼
Text Chunking
        │
        ▼
MiniLM-L6-v2 Embeddings
        │
        ▼
ChromaDB Vector Database
        │
        ▼
User Question
        │
        ▼
Similarity Search
        │
        ▼
Relevant Document Chunks Retrieved
        │
        ▼
LLM Generates Answer
        │
        ▼
Response in Streamlit Chat UI
🛠️ Tech Stack

Python

Streamlit – Frontend interface

LangChain

ChromaDB – Vector database

Sentence Transformers

MiniLM-L6-v2 Embedding Model

📂 Project Structure
streamlit-rag-document-chatbot
│
├── app.py                # Streamlit frontend with chat UI
├── rag_pipeline.py      # RAG logic (embeddings + vector DB + retrieval)
├── requirements.txt
├── README.md
└── chroma_db/           # Vector database storage
⚙️ Installation
1️⃣ Clone the repository
git clone https://github.com/yourusername/streamlit-rag-document-chatbot.git
cd streamlit-rag-document-chatbot
2️⃣ Install dependencies
pip install -r requirements.txt
3️⃣ Run the application
streamlit run app.py

💬 How to Use

Launch the Streamlit app

Upload a PDF or DOC/DOCX file

The document is processed and stored in ChromaDB

Ask questions in the chat window

The chatbot retrieves relevant document sections and answers your query

📌 Example Questions

Summarize this document
What are the key points discussed?
Explain the introduction section
What conclusion does the document provide?

🎯 Learning Objectives

This project demonstrates:

Retrieval-Augmented Generation (RAG)
Vector embeddings
Semantic search
LLM-powered document QA
Streamlit AI applications

📜 License
This project is for educational purposes.
