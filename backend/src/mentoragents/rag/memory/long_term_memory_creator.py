from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_mongodb.retrievers import MongoDBAtlasHybridSearchRetriever
from mentoragents.rag.retrievers import Retriever
from mentoragents.rag.splitters import TextSplitter
from mentoragents.core.config import settings
from mentoragents.models.mentor import Mentor
from loguru import logger
from mentoragents.db.client import MongoClientWrapper
from mentoragents.rag.extracter import Extracter
from mentoragents.rag.deduplicate_documents import DeduplicateDocuments
from mentoragents.db.indexes import MongoIndex
from mentoragents.models.mentor_extract import MentorExtract

class LongTermMemoryCreator:
    def __init__(self, retriever : MongoDBAtlasHybridSearchRetriever, splitter : RecursiveCharacterTextSplitter) -> None:
        self.retriever = retriever
        self.splitter = splitter
        self.deduplicate_documents = DeduplicateDocuments()
        self.extractor = Extracter()
        self.mongo_client_wrapper = MongoClientWrapper(
            model = Document, 
            collection_name = settings.MONGO_LONG_TERM_MEMORY_COLLECTION,
            database_name = settings.MONGO_DB_NAME,
            mongodb_uri = settings.MONGO_URI
        )

    @classmethod
    def build(cls) -> "LongTermMemoryCreator":
        retriever = Retriever(
            embedding_model_id = settings.RAG_TEXT_EMBEDDING_MODEL_ID,
            k = settings.RAG_TOP_K,
            device = settings.RAG_DEVICE
        ).get_hybrid_search_mongodb_retriever()

        splitter = TextSplitter(
            chunk_size = settings.RAG_CHUNK_SIZE,
        ).get_splitter()

        return cls(retriever, splitter)
    
    def __call__(self, mentors : list[MentorExtract]) -> None:
        if len(mentors) == 0:
            logger.warning("No mentors to extract. Exiting...")
        
        # First clear the long term memory collection to avoid duplicates
        logger.info("Clearing long term memory collection")
        self.mongo_client_wrapper.clear_collection()
        logger.info("Long term memory collection cleared")

        # Extract documents from sources
        logger.info("Extracting documents from sources")
        extraction_generator = self.extractor.get_extraction_generator(mentors)
        logger.info("Documents extracted from sources")

        # Ingest documents into the long term memory collection
        logger.info("Ingesting documents into the long term memory collection")
        for _, docs in extraction_generator:
            chunked_docs = self.splitter.split_documents(docs)
            chunked_docs = self.deduplicate_documents.remove_duplicates(chunked_docs)
            self.retriever.vectorstore.add_documents(chunked_docs)
        logger.info("Documents ingested into the long term memory collection")

        # Create index
        logger.info("Creating index")
        self.__create_index()
        logger.info("Index created")

    def __create_index(self) -> None:
        with self.mongo_client_wrapper as client:
            self.index = MongoIndex(
                retriever = self.retriever,
                client = client
            )
            self.index.create(
                is_hybrid = True,
                embedding_dim = settings.RAG_TEXT_EMBEDDING_MODEL_DIM
            )