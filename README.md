# 📄 RAG-Based Document Question Answering System

An AI-powered document question-answering system built using **Retrieval-Augmented Generation (RAG)**. Users can upload a PDF and ask questions about its content through an interactive Streamlit interface.

## 🚀 Features

- 📄 Upload PDF documents
- 🔍 Extract text from documents
- ✂️ Split documents into overlapping chunks
- 🧠 Generate semantic embeddings using Sentence Transformers
- 📦 Store and retrieve relevant document chunks
- 🔎 Perform similarity-based semantic search
- 💬 Ask natural-language questions about uploaded documents
- 🔗 Extract information such as GitHub, LinkedIn, and email
- 📚 Display retrieved sources and similarity scores
- 🎨 Interactive Streamlit web interface

## 🛠️ Technologies Used

- Python
- Streamlit
- Sentence Transformers
- PyPDF
- NumPy
- PyTorch
- Vector Similarity Search
- Retrieval-Augmented Generation (RAG)

## 🧠 How It Works

```text
PDF Upload
    ↓
Text Extraction
    ↓
Document Chunking
    ↓
Text Embeddings
    ↓
Vector Indexing
    ↓
Semantic Similarity Search
    ↓
Relevant Context Retrieval
    ↓
Question Answering
    ↓
Answer + Retrieved Sources