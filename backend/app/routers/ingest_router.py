from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from app.services.ingest_service import IngestService, get_ingest_service

ingest_router = APIRouter()

@ingest_router.websocket("/ingest")
async def ingest_documents(
    websocket: WebSocket,
    ingest_service: IngestService = Depends(get_ingest_service)
):
    """
    WebSocket endpoint for ingesting documents.

    This endpoint handles WebSocket connections for ingesting documents from the source directory.
    It uses the IngestService to load documents from the directory, process them, and provide
    real-time updates on the progress via WebSocket messages.

    Args:
        websocket (WebSocket): The WebSocket connection instance.
        ingest_service (IngestService): The service responsible for document ingestion, 
            provided by dependency injection.

    Raises:
        WebSocketDisconnect: Raised when the WebSocket connection is disconnected unexpectedly.
    """
    await websocket.accept()
    try:
        source_directory = "source_documents/"
        documents = await ingest_service.load_documents_from_directory(source_directory, websocket)
        await ingest_service.process_documents(documents, websocket)
        await websocket.send_text("Successfully ingested data!")
    except WebSocketDisconnect:
        print("WebSocket disconnected")
    except Exception as e:
        await websocket.send_text(f"Error: {e}")
    finally:
        await websocket.close()
