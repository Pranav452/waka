## Project Overview

This project consists of two independent components:

1. **Basic RAG (Retrieval-Augmented Generation):**
   - Implements a simple RAG system using FAISS for vector storage.
   - User data is provided in `knowledge.txt`, and the RAG system answers questions based on this data.

2. **API Endpoints:**
   - Provides several example API endpoints (see `route.py`).
   - These endpoints are not connected to the RAG system or to each other.
   - There is no database schema or relational structure; endpoints are for demonstration purposes only.
   - You can view and interact with these endpoints in the automatically generated API documentation.

**Note:**  
There is no integration between the RAG component and the API endpoints.  
Before running either component, please refer to `requirements.txt` to ensure all dependencies are installed.  
You can use the API documentation to explore the endpoints, or run the RAG system to interact with the knowledge base.