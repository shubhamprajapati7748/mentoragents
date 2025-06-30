from mentoragents.rag.memory.long_term_memory_creator import LongTermMemoryCreator
from mentoragents.models.mentor_factory import MentorFactory
import click
from pathlib import Path
from mentoragents.core.config import settings
from mentoragents.models.mentor_extract import MentorExtract

@click.command()
@click.option(
    "--metadata-file",
    type=click.Path(exists=True, path_type=Path),
    default=settings.EXTRACTION_METADATA_FILE_PATH,
    help="Path to the financial mentors extraction metadata JSON file.",
)
def main(metadata_file : Path) -> None:
    """CLI command to create long-term memory for financial mentors.
    
    Args:
        metadata_file : Path to the mentor extraction metadata JSON file.
    """
    mentors = MentorExtract.from_json(metadata_file)
    long_term_memory_creator = LongTermMemoryCreator.build()
    long_term_memory_creator(mentors)

if __name__ == "__main__":
    main()