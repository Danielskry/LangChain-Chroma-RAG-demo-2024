# LangChain Chroma RAG demo 2024

This repository demonstrates a Retrieval-Augmented Generation (RAG) system built with FastAPI, LangChain, and the ChromaDB vector database. The FastAPI app follows a Service-Oriented Architecture (SOA) and runs with an in-memory database that includes persistence. It allows users to ingest custom data and query it using a retriever and prompt template, with answers streamed back to the user in real time.

The illustration below is based on synthetic data generated from the documents included in the solution. It is used to demonstrate how queries can be made for troubleshooting maintenance logs.

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
