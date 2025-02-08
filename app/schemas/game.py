from pydantic import BaseModel

class GameResponse(BaseModel):
    idGame: int
    title: str
    description: str
    image: bytes
    details: str
    release: str