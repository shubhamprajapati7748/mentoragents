from fastapi import FastAPI
from contextlib import asynccontextmanager
from mentoragents.core.config import settings
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse 
import uvicorn
from mentoragents.core.config import Settings
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from mentoragents.core.exceptions import PermissionException, NotFoundException
from mentoragents.core.handlers import validation_exception_handler, permission_exception_handler, not_found_exception_handler

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles startup and shutdown events for the API."""
    # Startup code (if any) goes here
    yield
    # Shutdown code goes here
    # opik_tracer = OpikTracer()
    # opik_tracer.flush()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url="/openapi.json",
    lifespan=lifespan,
    redirect_slashes=False,  # Critical: disable FastAPI's built-in slash redirects
)

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


if __name__ == "__main__":
    settings = Settings()
    uvicorn.run(
        "mentoragents.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_config=None,  # We use structlog for logging
    ) 