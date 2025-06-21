from typing import Optional
from pydantic import ValidationError 

class PermissionException(Exception):
    """Exception raised when a user does not have a neccesaary permission to perform an action."""

    def __init__(
            self, 
            message : Optional[str] = "User does not have the right to perform this action",
    ):
        """Create a new PermissionException instance.

        Args:
        ----
            message (str, optional): The error message. Has default message.
        """
        self.message = message
        super().__init__(self.message)

class NotFoundException(Exception):
    """Exception raised when an object is not found."""
    def __init__(
            self, message : Optional[str] = "Object not found"
    ):
        """Create a new NotFoundException instance.

        Args:
        ----
            message (str, optional): The error message. Has default message.
        """
        self.message = message
        super().__init__(self.message)

def unpack_validation_error(exc : ValidationError) -> dict: 
    """Unpack a Pydantic validation error into a dictionary.

    Args:
    --- 
        exc (ValidationError): The Pydantic validation error.

    Returns:
    -------
        dict: The dictionary representation of the validation error.
    """
    error_messages = []
    for error in exc.errors():
        field = ".".join(str(loc) for loc in error["loc"])  
        message = error["msg"]
        error_messages.append({field: message})

    return {"errors": error_messages}