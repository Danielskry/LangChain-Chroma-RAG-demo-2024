from fastapi import WebSocket, WebSocketDisconnect, Depends
from typing import Any
import json

from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_community.vectorstores import Chroma

from app.core.environment import get_environment
from app.config import config as app_config
from app.core.logger import get_logger

logger = get_logger(__name__)

class RetrieverService:
    """
    A service class for managing document retrieval and question-answering (QA)
    using language models and vector databases.
    """

    def __init__(self):
        """
        Initializes the RetrieverService with environment configurations, language model, and embeddings.

        Raises:
            KeyError: If the environment is not found in the application configuration.
            RuntimeError: If the language model or embeddings cannot be retrieved.
        """
        environment = get_environment()
        logger.debug(f"Current environment: {environment}")

        if environment not in app_config:
            raise KeyError(f"Environment {environment} not found in app_config")

        self.ENVIRONMENT = app_config[environment]
        self.LLM = self.ENVIRONMENT.LLM.llm
        self.EMBEDDINGS = self.ENVIRONMENT.EMBEDDINGS.embeddings

        if self.LLM is None:
            raise RuntimeError("Failed to retrieve the language model!")
        
        if self.EMBEDDINGS is None:
            raise RuntimeError("Failed to retrieve embeddings model!")

        logger.debug(f"Initialized RetrieverService with environment: {self.ENVIRONMENT}")
    
    def create_chroma_retriever(self) -> Any:
        """
        Creates a retriever instance using LangChain's Chroma vector store.

        Returns:
            Any: A retriever instance configured for similarity-based retrieval.
        """
        persist_directory = 'chroma_db'
        embeddings = self.EMBEDDINGS
        chroma_db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
        retriever = chroma_db.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"score_threshold": 0.3}
        )
        return retriever

    @staticmethod
    def create_prompt_template() -> PromptTemplate:
        """
        Creates a prompt template for the question-answering task.

        Returns:
            PromptTemplate: A configured prompt template for generating answers.
        """
        template =  """
                        You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question.
                        If you don't know the answer, just say that you don't know. Answer concise.

                        Question: {question} 

                        Context: {context} 

                        Answer:
                    """
        return PromptTemplate(template=template, input_variables=["context", "question"])

    async def handle_retrieval(self, websocket: WebSocket, retriever: Any, prompt_template: PromptTemplate):
        """
        Handles document retrieval and question-answering over a WebSocket connection.

        Args:
            websocket (WebSocket): The WebSocket connection instance.
            retriever (Any): The retriever instance for fetching relevant documents.
            prompt_template (PromptTemplate): The prompt template for formatting questions and context.

        Raises:
            WebSocketDisconnect: If the WebSocket connection is disconnected unexpectedly.
        """
        retrieval_qa = RetrievalQA.from_chain_type(
            llm=self.LLM,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": prompt_template, 'verbose': True}
        )
        
        rag_chain_from_docs = (
            prompt_template
            | self.LLM
            | StrOutputParser()
        )

        while True:
            try:
                logger.info("Waiting for query from client")
                query = await websocket.receive_text()
                logger.info(f"Received query: {query}")
                if query:
                    rag_chain_with_source = RunnableParallel(
                        {
                            "context": retriever,
                            "question": RunnablePassthrough()
                        }
                    ).assign(answer=rag_chain_from_docs)
            
                    response_stream = rag_chain_with_source.stream(query)
                    full_response = ""
                    for chunk in response_stream:
                        logger.info(f"Received chunk: {chunk} (type: {type(chunk)})")
                        
                        if chunk := chunk.get("answer"):
                            full_response += chunk
                            await websocket.send_text(chunk)
                    
                    # Send the full response once completed
                    await websocket.send_text(f"Full response: {full_response}")

                    logger.info("Query processing completed.")
            except WebSocketDisconnect:
                logger.info("WebSocket disconnected during retrieval")
                break
            except Exception as e:
                logger.error(f"Exception during retrieval: {e}")
                await websocket.send_text(json.dumps({"error": str(e)}))
                break


def get_retriever_service() -> RetrieverService:
    """
    Factory function to get an instance of RetrieverService.

    Returns:
        RetrieverService: An instance of RetrieverService.
    """
    return RetrieverService()
