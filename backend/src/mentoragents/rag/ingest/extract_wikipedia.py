from langchain_core.documents import Document
from langchain_community.document_loaders import WikipediaLoader
from loguru import logger
from mentoragents.models.mentor_extract import MentorExtract

def extract_wikipedia(mentor_extract : MentorExtract) -> list[Document]:
        """Extract documents from  Wikipredia for a given mentor.

        Args:
            mentor : Mentor object containing mentor details.

        Returns:
            list[Document] : List of documents extracted from Wikipedia.
        """
        logger.info(f"Extracting docs from Wikipedia for {mentor_extract.name}")
        data_loader = WikipediaLoader(
            query = mentor_extract.name,
            lang = "en",
            load_max_docs = 10,
            doc_content_chars_max = 1000000,
        )

        docs = data_loader.load()

        for doc in docs:
            doc.metadata["mentor_id"] = mentor_extract.id
            doc.metadata["mentor_name"] = mentor_extract.name
            doc.metadata["source_url"] = doc.metadata["source"]
            doc.metadata["source"] = "wikipedia"
        logger.info(f"Extracted {len(docs)} docs from Wikipedia for {mentor_extract.name}")
        return docs 