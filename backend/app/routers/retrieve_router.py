from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from app.services.retrieve_service import RetrieverService, get_retriever_service
from app.core.logger import get_logger

logger = get_logger(__name__)

retrieve_router = APIRouter()

@retrieve_router.websocket("/retrieve")
async def retrieve_query(
    websocket: WebSocket,
    retriever_service: RetrieverService = Depends(get_retriever_service)
):
    """
    WebSocket endpoint for handling document retrieval queries.

    This endpoint manages WebSocket connections to receive queries, process them using the retriever service,
    and return results to the client. It leverages the RetrieverService to create a retriever and a prompt template,
    then handles the retrieval process, sending results back to the client in real-time.

    Args:
        websocket (WebSocket): The WebSocket connection instance.
        retriever_service (RetrieverService): The service for handling retrieval operations,
            provided by dependency injection.

    Raises:
        WebSocketDisconnect: Raised when the WebSocket connection is unexpectedly closed.
        Exception: Catches all other exceptions, logs them, and sends an error message to the client.
    """
    await websocket.accept()
    logger.info("WebSocket connection accepted")

    try:
        retriever = retriever_service.create_chroma_retriever()
        prompt_template = retriever_service.create_prompt_template()
        await retriever_service.handle_retrieval(websocket, retriever, prompt_template)
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")
    except Exception as e:
        logger.error(f"Exception: {e}")
        await websocket.send_text(f"Error: {e}")
    finally:
        try:
            await websocket.close()
            logger.info("WebSocket connection closed")
        except RuntimeError as re:
            logger.error(f"RuntimeError on close: {re}")
