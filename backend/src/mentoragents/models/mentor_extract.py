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
        name (str) : Name of the mentor.
        expertise (str) : Expertise of the mentor.
        perspective (str) : Perspective of the mentor.
        style (str) : Style of the mentor.
        image_url (str) : Image URL of the mentor.
        twitter_handle (str) : Twitter handle of the mentor.
        pdf (List[str]) : List of PDF URLs with information about the mentor.
    """
    id : str = Field(description = "Unique identifier for the mentor")
    name : str = Field(description = "Name of the mentor")
    expertise : str = Field(description = "Expertise of the mentor")
    perspective : str = Field(description = "Perspective of the mentor")
    style : str = Field(description = "Style of the mentor")
    image_url : str = Field(description = "Image URL of the mentor")
    twitter_handle : str = Field(description = "Twitter handle of the mentor")
    pdf : List[str] = Field(description = "List of PDF URLs with information about the mentor")
    websites : List[str] = Field(description = "List of websites with information about the mentor")
    youtube_videos : List[str] = Field(description = "List of YouTube videos with information about the mentor")

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