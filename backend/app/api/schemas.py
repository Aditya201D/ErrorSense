from pydantic import BaseModel

class UserInput(BaseModel):
    request: str = ""
    response: str = ""