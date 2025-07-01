from langchain.tools.retriever import create_retriever_tool 
from mentoragents.core.config import settings 
from mentoragents.rag.retrievers import Retriever 
from loguru import logger

class Tools:
    """
    A class that contains the tools for the Model response.
    """
    def __init__(self):
        """
        Initialize the tools.
        """
        retriever = Retriever(
            embedding_model_id = settings.RAG_TEXT_EMBEDDING_MODEL_ID,
            k = settings.RAG_TOP_K,
            device = settings.RAG_DEVICE
        )
        self.mongodb_retriever = retriever.get_hybrid_search_mongodb_retriever()

        self.retriever_tool = create_retriever_tool(
            self.mongodb_retriever, 
            name = "retrieve_mentor_context", 
            description = "Search and return information about the specific mentor. Always use this tool when the user asks about the mentor's background, expertise, or any other information related to the mentor.")

    def get_tools(self):
        """
        Get the tools.
        """
        return [self.retriever_tool]