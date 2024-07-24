from pydantic import BaseModel

class Status(BaseModel):
    """ Status message for server. """
    status: str
    message: str
