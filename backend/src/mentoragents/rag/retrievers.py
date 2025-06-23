from .embeddings import Embeddings
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_mongodb.retrievers import MongoDBAtlasVectorSearchRetriever 
from loguru import logger  
from src.mentoragents.core.config import settings 

class Retriever:
    """
    A class that retrieves documents from the MongoDB Atlas vector search.
    """
    def __init__(self, embedding_model_id : str, k : int = 3, device : str = "cpu"):
        """
        Initializes the Retriever with an embedding model and a k value.
        """
        self.k = k
        self.embeddings_model = Embeddings(embedding_model_id, device).get_hf_model()

    def get_mongodb_retriever(self):
        """
        Returns a MongoDBAtlasVectorSearchRetriever object that retrieves documents from the MongoDB Atlas vector search.
        """
        logger.info(f"Initializing MongoDBAtlasVectorSearchRetriever with embedding model: {self.embeddings_model_id} and k: {self.k}")
        vector_store = MongoDBAtlasVectorSearch.from_connection_string(
            connection_string = settings.MONGODB_CONNECTION_STRING,
            namespace = f"{settings.MONGODB_NAMESPACE}.{settings.MONGO_LONG_TERM_MEMORY_COLLECTION}",
            text_key = "chunk",
            embedding_key = "embedding",
            relevance_score_fn = "dotProduct"
        )
        retriever = MongoDBAtlasVectorSearchRetriever(
            vector_store = vector_store,
            search_index_name = "hybrid_search_index",
            embedding_model = self.embeddings_model,
            k = self.k,
            vector_penalty = 50,
            fulltext_penalty = 50,
        )
        return retriever






    
    