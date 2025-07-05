from typing import Optional
from pydantic_settings import BaseSettings 
from pydantic import Field, field_validator
from pydantic_settings import SettingsConfigDict
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """Pydantic settings class.

    Attributes:
    ----------
        PROJECT_NAME (str): The name of the project.
        LOCAL_DEVELOPMENT (bool): Whether the application is running locally.
        ENVIRONMENT (str): The deployment environment (local, dev, test, prod).
        GROQ_API_KEY (str): The API key for the GROQ service.
        GROQ_LLM_MODEL (str): The model to use for the GROQ service.
        GROQ_LLM_MODEL_CONTEXT_SUMMARY (str): The model to use for the GROQ service context summary.
        OPENAI_API_KEY (str): The API key for the OpenAI service.   
        MONGO_URI (str): The URI for the MongoDB service.
        MONGO_DB_NAME (str): The name of the MongoDB database.
        MONGO_STATE_CHECKPOINT_COLLECTION (str): The name of the MongoDB collection for state checkpoints.
        MONGO_STATE_WRITES_COLLECTION (str): The name of the MongoDB collection for state writes.
        MONGO_LONG_TERM_MEMORY_COLLECTION (str): The name of the MongoDB collection for long term memory.
        COMET_API_KEY (str): The API key for the Comet ML and Opik services.
        COMET_PROJECT (str): The project name for the Comet ML and Opik services.
        TOTAL_MESSAGES_SUMMARY_TRIGGER (int): The number of messages to trigger a summary.
        TOTAL_MESSAGES_AFTER_SUMMARY (int): The number of messages after which to trigger a summary.
        RAG_TEXT_EMBEDDING_MODEL_ID (str): The ID of the text embedding model.
        RAG_TEXT_EMBEDDING_MODEL_DIM (int): The dimension of the text embedding model.
        RAG_TOP_K (int): The number of top results to return.
        RAG_DEVICE (str): The device to use for the RAG service.
        RAG_CHUNK_SIZE (int): The chunk size for the RAG service.
        EVALUATION_DATASET_FILE_PATH (Path): The path to the evaluation dataset file.
        EXTRACTION_METADATA_FILE_PATH (Path): The path to the extraction metadata file.
        ARCADE_API_KEY (str): The API key for the Arcade services.
        ARCADE_USER_ID (str): The Twitter user ID for the Arcade services.
        LANGSMITH_API_KEY (str): The API key for the LangSmith services.
        LANGSMITH_TRACING (bool): Whether to enable tracing for the LangSmith services.
        LANGSMITH_ENDPOINT (str): The endpoint for the LangSmith services.
        LANGSMITH_PROJECT (str): The project name for the LangSmith services.
    """

    PROJECT_NAME : str = "MentorAgents"
    LOCAL_DEVELOPMENT : bool = False
    ENVIRONMENT : str = "local" 

    APP_VERSION : str = "0.1.0"
    DEBUG : bool = False
    
    # Server settings
    HOST : str = "0.0.0.0"
    PORT : int = 8000
    RELOAD : bool = True
    

    # --- GROQ Configuration ---
    GROQ_API_KEY : str 
    GROQ_LLM_MODEL : str = "llama-3.3-70b-versatile"
    GROQ_LLM_MODEL_CONTEXT_SUMMARY : str = "llama-3.1-8b-instant"
    
    # --- OpenAI Configuration (Required for evaluation) ---
    OPENAI_API_KEY : str 
    OPENAI_LLM_MODEL : str = "gpt-4o-mini"

    # --- MongoDB Configuration ---
    MONGO_URI : str = Field(
        default="mongodb://mentor_user:mentor_password@localhost:27017/?directConnection=true",
        description="Connection URI for the local MongoDB Atlas instance.",
    )
    MONGO_DB_NAME : str = "mentoragents"
    MONGO_MENTORS_COLLECTION : str = "mentors"
    MONGO_STATE_CHECKPOINT_COLLECTION : str = "mentor_state_checkpoints"
    MONGO_STATE_WRITES_COLLECTION : str = "mentor_state_writes"
    MONGO_LONG_TERM_MEMORY_COLLECTION : str = "mentor_long_term_memory"

    # --- Comet ML & Opik Configuration ---
    COMET_API_KEY : str | None = Field(
        default=None, description="API key for Comet ML and Opik services."
    )

    COMET_PROJECT : str = Field(
        default="mentor_agents",
        description="Project name for Comet ML and Opik tracking.",
    )

    # --- Agents Configuration ---
    TOTAL_MESSAGES_SUMMARY_TRIGGER : int = 30 
    TOTAL_MESSAGES_AFTER_SUMMARY : int = 5 

    # --- RAG Configuration ---
    RAG_TEXT_EMBEDDING_MODEL_ID : str = "sentence-transformers/all-MiniLM-L6-v2"
    RAG_TEXT_EMBEDDING_MODEL_DIM : int = 384
    RAG_TOP_K : int = 3
    RAG_DEVICE : str = "cpu"
    RAG_CHUNK_SIZE : int = 256
    RAG_CHUNK_OVERLAP : int = 10 

    # --- CORS Configuration ---
    ADDITIONAL_CORS_ORIGINS: Optional[str] = None  # Separated by commas or semicolons
    @field_validator("ADDITIONAL_CORS_ORIGINS", mode="before")
    def parse_cors_origins(cls, v: Optional[str]) -> Optional[list[str]]:
        """Parse CORS origins from string to list, supporting both comma and semicolon separators.

        Args:
            v: The CORS origins string or list.

        Returns:
            Optional[list[str]]: The parsed list of CORS origins or None.
        """
        if isinstance(v, list) or v is None:
            return v

        if ";" in v:
            return [origin.strip() for origin in v.split(";") if origin.strip()]

        # Default Pydantic behavior will handle comma separation
        return v

    # --- Paths Configuration ---
    EXTRACTION_METADATA_FILE_PATH : Path = Path("data/extraction_metadata.json")
    EVALUATION_DATASET_FILE_PATH : Path = Path("data/evaluation_dataset.json")

    # --- Arcade Configuration ---
    ARCADE_API_KEY : str
    ARCADE_USER_ID : str

    # --- LangSmith Configuration ---
    LANGSMITH_API_KEY : str
    LANGSMITH_TRACING : str = "true"
    LANGSMITH_ENDPOINT : str = "https://api.smith.langchain.com"
    LANGSMITH_PROJECT : str = "mentoragents"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

settings = Settings()