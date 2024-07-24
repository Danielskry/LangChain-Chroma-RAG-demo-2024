# LangChain Chroma RAG demo 2024

This repository demonstrates a Retrieval-Augmented Generation (RAG) system using FastAPI, LangChain, and the ChromaDB vector database. The system runs with an in-memory with persistance database. It allows users to ingest custom data and query it using a retriever and prompt template, with answers streamed back to the user.

The illustration below is based on synthetic data derived from the documents included in the solution. It is used to demonstrate how troubleshooting from maintenance logs can be queried.

![ezgif-1-bfac569373](https://github.com/user-attachments/assets/170bfbd0-81e7-4f1d-acf5-3321043ae2ed)

## Getting Started
### Prerequisites
- Docker
- OpenAI API key

### Setup
1. **Configure Environment Variables**
   - Rename `backend/.env.example` to `.env`.
   - Enter your OpenAI API key in the `.env` file.
2. **Add Your Data**
   - Place your documents in the `backend/source_documents` directory.
3. **Build and Start the Application**
   - Use Docker to build and launch the application:
    ```bash
    docker-compose up --build -d
    ```
4. **Access the Frontend**
   - Once the application is running, access the frontend interface at http://localhost:8501/.
