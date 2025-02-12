from pydantic import BaseModel

class UserRequest(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    idUser: int
    username: str
    password: str
    token: str