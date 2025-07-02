from langchain_core.documents import Document 
from mentoragents.models.mentor import Mentor
from typing import Generator
from tqdm import tqdm
from mentoragents.models.mentor_factory import MentorFactory
from loguru import logger
from mentoragents.models.mentor_extract import MentorExtract
from mentoragents.rag.ingest.extract_wikipedia import extract_wikipedia
from mentoragents.rag.ingest.extract_twitter_tweets import extract_twitter_tweets
from mentoragents.rag.ingest.extract_pdf_contents import extract_pdf_contents

class Extracter:
    def __init__(self):
        pass

    def extract(self, mentor_extract : MentorExtract) -> list[Document]:
        """Extract documents for a single mentor from all the sources and duduplicats them. 

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
        logger.info(f"Extracted {len(docs)} docs for {mentor_extract.name}")
        return docs 
    
    def get_extraction_generator(
            self, mentors : list[MentorExtract]
    ) -> Generator[tuple[Mentor, list[Document]], None, None]:
        """Extract documents from a list of philosophers, yielding one at a time.
        
        Args:
            mentors : A list of MentorExtract objects containing mentor information.

        Yields:
            tuple[Mentor, list[Document]] : A tuple containing the mentor and the list of documents extracted from the mentor.
        """
        
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
            docs = self.extract(mentor_extract)
            mentor = Mentor(
                id = mentor_extract.id,
                mentor_name = mentor_extract.name,
                mentor_expertise = mentor_extract.expertise,
                mentor_perspective = mentor_extract.perspective,
                mentor_style = mentor_extract.style,
            )
            yield mentor, docs

        progress_bar.close()

# if __name__ == "__main__":
#     # naval_ravikant = MentorFactory().get_financial_mentor("naval_ravikant")
#     # docs = Extracter().extract(naval_ravikant)
#     # print(docs)
