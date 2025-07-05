from langchain_core.documents import Document 
from mentoragents.models.mentor import Mentor
from typing import Generator
from tqdm import tqdm
from loguru import logger
from mentoragents.models.mentor_extract import MentorExtract
from mentoragents.rag.extractors.extract_wikipedia import extract_wikipedia
from mentoragents.rag.extractors.extract_twitter_tweets import extract_twitter_tweets
from mentoragents.rag.extractors.extract_pdf_contents import extract_pdf_contents
from mentoragents.rag.extractors.extract_youtube_transcripts import extract_youtube_transcripts
from mentoragents.db.client import MongoClientWrapper
from mentoragents.core.config import settings

class Extractor:
    def __init__(self):
        self.mentors_collection = MongoClientWrapper(
            model = MentorExtract,
            collection_name = settings.MONGO_MENTORS_COLLECTION,
            database_name = settings.MONGO_DB_NAME,
            mongodb_uri = settings.MONGO_URI
        )

    def extract(self, mentor_extract : MentorExtract) -> list[Document]:
        """Extract documents for a single mentor from all the sources and deduplicates them. 

        Args:
            mentor : Mentor object containing mentor details.

        Returns:
            list[Document] : List of deduplicated documents extracts for the mentor.
        """ 
        logger.info(f"Extracting docs for {mentor_extract.name}")
        docs = []
        docs.extend(extract_wikipedia(mentor_extract))
        docs.extend(extract_twitter_tweets(mentor_extract))
        docs.extend(extract_pdf_contents(mentor_extract))
        docs.extend(extract_youtube_transcripts(mentor_extract))
        logger.info(f"Extracted {len(docs)} docs for {mentor_extract.name}")
        return docs 
    
    def extract_sample_docs(self, mentor_extract : MentorExtract, sample_count : int = 2) -> list[Document]:
        """Extract sample documents for a mentor from all the sources and deduplicates them.

        Args:
            mentor_extract : MentorExtract object containing mentor details.
            sample_count : The number of samples to extract.

        Returns:
            list[Document] : List of deduplicated sample documents for the mentor.
        """
        logger.info(f"Extracting sample data for {mentor_extract.id}")
        docs = []
        wikipedia_docs = extract_wikipedia(mentor_extract)
        twitter_docs = extract_twitter_tweets(mentor_extract)
        pdf_docs = extract_pdf_contents(mentor_extract)
        youtube_docs = extract_youtube_transcripts(mentor_extract)
        docs.extend(wikipedia_docs[:sample_count])
        docs.extend(twitter_docs[:sample_count])
        docs.extend(pdf_docs[:sample_count])
        docs.extend(youtube_docs[:sample_count])
        logger.info(f"Extracted {len(docs)} sample docs for {mentor_extract.id}")
        return docs
        
    def get_extraction_generator(
            self,
            is_sample_data : bool = False,
            sample_count : int = 2
    ) -> Generator[tuple[Mentor, list[Document]], None, None]:
        """Extract documents from a list of philosophers, yielding one at a time.
        
        Args:
            is_sample_data : Whether to extract sample data.
            sample_count : The number of samples to extract.

        Yields:
            tuple[Mentor, list[Document]] : A tuple containing the mentor and the list of documents extracted from the mentor.
        """

        # Fetch all mentors from the mentors collection
        logger.info("Fetching all mentors from the mentors collection")
        mentors = self.mentors_collection.fetch_documents(query = {}, limit = None)
        logger.info(f"Fetched {len(mentors)} mentors from the mentors collection")

        progress_bar = tqdm(
            mentors, 
            desc = "Extracting docs",
            unit = "mentor",
            bar_format="{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}] {postfix}",
            ncols=100,
            position=0,
            leave=True,
        )

        for mentor_extract in progress_bar:
            progress_bar.set_postfix({"mentor": mentor_extract.name})
            docs = []
            if is_sample_data:
                docs = self.extract_sample_docs(mentor_extract, sample_count)
            else:
                docs = self.extract(mentor_extract)
            
            mentor = Mentor(
                id = mentor_extract.id,
                mentor_name = mentor_extract.name,
                mentor_expertise = mentor_extract.expertise,
                mentor_perspective = mentor_extract.perspective,
                mentor_style = mentor_extract.style,
            )

            logger.info(f"Saving mentor into mongoDB")
            yield mentor, docs

        progress_bar.close()