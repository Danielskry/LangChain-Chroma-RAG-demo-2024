# LangChain Chroma RAG demo 2024

This repository demonstrates a Retrieval-Augmented Generation (RAG) system using FastAPI, LangChain, and the ChromaDB vector database. The system runs with an in-memory database and includes persistence capabilities. It allows users to ingest custom data and query it using a retriever and prompt template, with answers streamed back to the user.

The screenshot below is based on synthetic data from the documents included in the solution. It is used to illustrate how it is possible to troubleshoot and analyze maintenance logs.

![bilde](https://github.com/user-attachments/assets/049c6a59-ac7c-4cb5-91ae-2846242c0a68)

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
