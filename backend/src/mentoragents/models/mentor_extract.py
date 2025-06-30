from pydantic import BaseModel, Field
from typing import List
from pathlib import Path
import json
from mentoragents.models.mentor import Mentor

class MentorExtract(BaseModel):
    """A class representing raw mentor data extracted from external sources.

    This class follows the structire of the mentors.json file and contains a basic information about mentor before enrichment. 

    Args:
        id (str) : Unique identifier for the mentor.
        urls (List[str]) : List of URLs with information about the mentor. 
    """
    id : str = Field(description = "Unique identifier for the mentor")
    urls : List[str] = Field(description = "List of URLs with information about the mentor")

    @classmethod
    def from_json(cls, metadata_file: Path) -> list["MentorExtract"]:
        with open(metadata_file, "r") as f:
            mentors_data = json.load(f)
            
        return [cls(**mentor) for mentor in mentors_data]
   
    # @classmethod 
    # def from_json(cls, metadata_file : Path) -> list["MentorExtract"] : 
    #     """Loads mentor extract data from a JSON file.

    #     Args:
    #         metadata_file (Path) : Path to the JSON file containing mentor extract data.

    #     Returns:
    #         list[MentorExtract] : List of MentorExtract objects loaded from the JSON file.
    #     """
    #     with open(metadata_file, "r") as f : 
    #         mentors_data = json.load(f)
    #     return [cls(**mentor) for mentor in mentors_data]