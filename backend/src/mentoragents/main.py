from fastapi import FastAPI,  HTTPException, Depends, WebSocket, WebSocketDisconnect
from mentoragents.core.config import settings
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse 
import uvicorn
from mentoragents.core.config import Settings
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from mentoragents.core.exceptions import PermissionException, NotFoundException
from mentoragents.core.handlers import validation_exception_handler, permission_exception_handler, not_found_exception_handler
from pydantic import BaseModel
from mentoragents.utils.generate_response import get_response, get_streaming_response
from mentoragents.utils.reset_conversation import reset_conversation_state
from mentoragents.models.mentor_factory import MentorFactory
from mentoragents.workflow.graph import MentorGraph

# Application state management 
class ApplicationState:
    def __init__(self):
        self.graph_builder = None
    
    async def initialize(self):
        graph = MentorGraph()
        self.graph_builder = graph.build()

    async def shutdown(self):
        self.graph_builder = None

class ChatMessage(BaseModel):
    message : str
    mentor_id : str

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url="/openapi.json",
    docs_url="/docs",
    description="AI agents, trained by the minds that move the world.",
    version="0.1.0",
    # lifespan=lifespan,
)

@app.on_event("startup")
async def startup_event():
    app.state.app_state = ApplicationState()
    await app.state.app_state.initialize()
    
@app.on_event("shutdown")
async def shutdown_event():
    await app.state.app_state.shutdown()

CORS_ORIGINS = [
    "http://localhost:5173",
    "localhost:8001",
    "http://localhost:8080",
    "localhost:3000",
]

if settings.ADDITIONAL_CORS_ORIGINS:
    additional_origins = settings.ADDITIONAL_CORS_ORIGINS.split(",")
    if settings.ENVIRONMENT == "local":
        CORS_ORIGINS.append("*")  # Allow all origins in local environment
    else:
        CORS_ORIGINS.extend(additional_origins)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency injection
async def get_graph_builder():
    return app.state.app_state.graph_builder

# Exception handlers
app.exception_handler(RequestValidationError)(validation_exception_handler)
app.exception_handler(ValidationError)(validation_exception_handler)
app.exception_handler(PermissionException)(permission_exception_handler)
app.exception_handler(NotFoundException)(not_found_exception_handler)

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def show_docs_reference() -> HTMLResponse:
    """Root endpoint to display the API documentation.

    Returns:
    -------
        HTMLResponse: The HTML content to display the API documentation.

    """
    html_content = """
<!DOCTYPE html>
<html>
    <head>
        <title>MentorAgents API</title>
    </head>
    <body>
        <h1>Welcome to the MentorAgents API</h1>
        <p>Please visit the <a href="https://docs.mentoragents.ai">docs</a> for more information.</p>
    </body>
</html>
    """
    return HTMLResponse(content=html_content)

@app.post("/chat")
async def chat(
    chat_messages : ChatMessage,
    graph_builder : MentorGraph = Depends(get_graph_builder)
):
    """
    Handle the chat message and return the response.
    """
    try:
        mentor = MentorFactory.get_financial_mentor(chat_messages.mentor_id)
        response, _ = await get_response(
            graph_builder = graph_builder,
            messages = chat_messages.message,
            mentor_id = chat_messages.mentor_id,
            mentor_name = mentor.mentor_name,
            mentor_expertise = mentor.mentor_expertise,
            mentor_perspective = mentor.mentor_perspective,
            mentor_style = mentor.mentor_style,
            mentor_context = ""
        )
        return {
            "response" : response,
        }
    except Exception as e : 
        raise HTTPException(status_code=500, detail=str(e))


@app.websocket("/ws/chat")
async def websocket_chat(
    websocket : WebSocket,
    graph_builder : MentorGraph = Depends(get_graph_builder)
):
    """
    Handle the websocket chat message and return the response.
    """
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()

            if "message" not in data or "mentor_id" not in data:
                await websocket.send_json({
                    "error" : "Invalid message format. Required fields : 'message' and 'mentor_id'"
                })
                continue 
        
            try:
                message = data["message"]
                mentor_id = data["mentor_id"]

                mentor = MentorFactory.get_financial_mentor(mentor_id)

                # Use streaming response to get the response
                streaming_response = get_streaming_response(
                    graph_builder = graph_builder,
                    messages = message,
                    mentor_id = mentor_id,
                    mentor_name = mentor.mentor_name,
                    mentor_expertise = mentor.mentor_expertise,
                    mentor_perspective = mentor.mentor_perspective,
                    mentor_style = mentor.mentor_style,
                    mentor_context = ""
                )

                # Send initial message to indicate streaming has started
                await websocket.send_json({"streaming" : True})

                # Stream each chunk of the response 
                async for chunk in streaming_response:
                    full_response += chunk 
                    await websocket.send_json({"chunk" : chunk})

                # Send final message to indicate streaming has ended
                await websocket.send_json({"streaming" : False, "response" : full_response})
            except Exception as e:
                await websocket.send_json({"error" : str(e)})
                break
            
    except WebSocketDisconnect:
        pass
    


@app.post("/reset-memory")
async def reset_memory():
    """
    Reset the conversation state. It deletes the two collections needed for the keeping short-term memory in MongoDB
    """
    try:
        result = await reset_conversation_state()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



if __name__ == "__main__":
    settings = Settings()
    uvicorn.run(
        "mentoragents.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_config=None,  # We use structlog for logging
    ) 

