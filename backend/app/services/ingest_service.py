import os
import glob
from typing import List
from fastapi import WebSocket
from langchain_community.document_loaders import (
    CSVLoader, EverNoteLoader, PDFMinerLoader, TextLoader,
    UnstructuredEPubLoader, UnstructuredHTMLLoader, UnstructuredMarkdownLoader,
    UnstructuredODTLoader, UnstructuredPowerPointLoader, UnstructuredWordDocumentLoader,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document
from langchain_community.vectorstores.chroma import Chroma

from app.core.environment import get_environment
from app.config import config as app_config
from app.core.logger import get_logger

logger = get_logger(__name__)

DOC_LOADERS_MAPPING = {
    ".csv": (CSVLoader, {}),
    ".doc": (UnstructuredWordDocumentLoader, {}),
    ".docx": (UnstructuredWordDocumentLoader, {}),
    ".enex": (EverNoteLoader, {}),
    ".epub": (UnstructuredEPubLoader, {}),
    ".html": (UnstructuredHTMLLoader, {}),
    ".md": (UnstructuredMarkdownLoader, {}),
    ".odt": (UnstructuredODTLoader, {}),
    ".pdf": (PDFMinerLoader, {}),
    ".ppt": (UnstructuredPowerPointLoader, {}),
    ".pptx": (UnstructuredPowerPointLoader, {}),
    ".txt": (TextLoader, {"encoding": "utf8"}),
}

class IngestService:
    """
    A service class for ingesting and processing documents using various loaders and embeddings.
    """

    def __init__(self):
        """
        Initializes the IngestService with environment configurations and embeddings.

        Raises:
            KeyError: If the environment is not found in the application configuration.
            RuntimeError: If embeddings cannot be retrieved.
        """
        environment = get_environment()
        logger.debug(f"Current environment: {environment}")

        if environment not in app_config:
            raise KeyError(f"Environment {environment} not found in app_config")

        self.ENVIRONMENT = app_config[environment]
        self.EMBEDDINGS = self.ENVIRONMENT.EMBEDDINGS.embeddings
        
        if self.EMBEDDINGS is None:
            raise RuntimeError("Failed to retrieve embeddings model!")

        logger.debug(f"Initialized IngestService with environment: {self.ENVIRONMENT}")

    def load_single_document(self, file_path: str) -> Document:
        """
        Loads a single document based on its file extension using the appropriate loader.

        Args:
            file_path (str): The path to the document file.

        Returns:
            Document: The loaded document.

        Raises:
            ValueError: If the file extension is unsupported.
        """
        ext = "." + file_path.rsplit(".", 1)[-1]
        logger.debug(f"Loading file '{file_path}' with extension '{ext}'")
        if ext in DOC_LOADERS_MAPPING:
            loader_class, loader_args = DOC_LOADERS_MAPPING[ext]
            loader = loader_class(file_path, **loader_args)
            document = loader.load()[0]
            logger.debug(f"Loaded document: {document}")
            return document
        logger.error(f"Unsupported file extension '{ext}'")
        raise ValueError(f"Unsupported file extension '{ext}'")

    async def load_documents_from_directory(self, source_dir: str, websocket: WebSocket) -> List[Document]:
        """
        Loads all documents from a specified directory using various loaders based on file extensions.

        Args:
            source_dir (str): The directory to load documents from.
            websocket (WebSocket): WebSocket connection for sending progress updates.

        Returns:
            List[Document]: A list of loaded documents.
        """
        logger.info(f"Loading documents from directory '{source_dir}'")
        absolute_source_dir = os.path.abspath(source_dir)
        logger.debug(f"Absolute source directory: {absolute_source_dir}")

        all_files = []
        for ext in DOC_LOADERS_MAPPING:
            files = glob.glob(os.path.join(absolute_source_dir, f"**/*{ext}"), recursive=True)
            logger.debug(f"Found {len(files)} files with extension '{ext}'")
            all_files.extend(files)

        documents = []
        total_files = len(all_files)
        logger.info(f"Total files to load: {total_files}")
        for i, file_path in enumerate(all_files):
            try:
                document = self.load_single_document(file_path)
                documents.append(document)
                logger.info(f"Loaded document {i+1}/{total_files}: '{file_path}'")
            except Exception as e:
                logger.error(f"Failed to load document '{file_path}': {e}")
            progress = (i + 1) / total_files * 100
            await websocket.send_text(f"Ingesting: {progress:.2f}% complete")

        logger.info("Completed loading all documents")
        return documents

    async def process_documents(self, documents: List[Document], websocket: WebSocket) -> None:
        """
        Processes a list of documents by splitting them into chunks and storing them in a vector database.

        Args:
            documents (List[Document]): The documents to process.
            websocket (WebSocket): WebSocket connection for sending progress updates.
        """
        logger.info("Processing documents")
        chunk_size = 500
        chunk_overlap = 50
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        texts = text_splitter.split_documents(documents)
        logger.debug(f"Split documents into {len(texts)} chunks")

        persist_directory = '/usr/src/app/backend/chroma_db'
        logger.info(f"Using persist directory: {persist_directory} ({os.path.abspath(persist_directory)})")
        
        if not os.path.exists(persist_directory):
            os.makedirs(persist_directory)
            logger.info(f"Created directory: {persist_directory}")

        try:
            vectordb = Chroma.from_documents(
                documents=texts,
                embedding=self.EMBEDDINGS,
                persist_directory=persist_directory
            )
            vectordb.persist()

            if os.path.exists(persist_directory):
                logger.info(f"Directory contents: {os.listdir(persist_directory)}")
            else:
                logger.error(f"Directory {persist_directory} does not exist after persisting.")
        except Exception as e:
            logger.error(f"Failed to create or persist vector database: {e}")

        logger.info(f"Persisted vector database at '{persist_directory}'")

def get_ingest_service() -> IngestService:
    """
    Factory function to get an instance of IngestService.

    Returns:
        IngestService: An instance of IngestService.
    """
    return IngestService()
