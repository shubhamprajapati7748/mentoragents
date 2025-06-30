from mentoragents.models.mentor import Mentor
from mentoragents.utils.constant_mentors import CONSTANT_FINANCIAL_MENTORS
from mentoragents.core.exceptions import MentorNotFoundException

class MentorFactory:

    @staticmethod 
    def get_financial_mentor(id : str) -> Mentor:
        """Create a mentor instance based on the provided ID. 

        Args: 
            id (str) : Unique identifier for the mentor.

        Returns: 
            Mentor : A Mentor object with the specified ID. 
        
        Raises:
            ValueError : If mentor ID is not found in the configuration.
        """
        id_lower = id.lower()
        if id_lower not in CONSTANT_FINANCIAL_MENTORS:
            raise MentorNotFoundException(f"Mentor with ID {id} not found")
        return CONSTANT_FINANCIAL_MENTORS[id_lower]

        
    @staticmethod
    def get_all_financial_mentors() -> list[Mentor]:
        """Get all financial mentors.

        Returns:
            list[Mentor] : A list of Mentor objects.
        """
        return list(CONSTANT_FINANCIAL_MENTORS.values())