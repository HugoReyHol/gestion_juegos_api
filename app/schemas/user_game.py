from pydantic import BaseModel
from typing import Optional

class UserGameScheme(BaseModel):
    idUser: int
    idGame: int
    score: Optional[int]
    timePlayed: int
    gameState: str
    lastChange: int

class UserGameUpdate(BaseModel):
    score: Optional[int] = None
    timePlayed: Optional[int] = None
    gameState: Optional[str] = None
    lastChange: Optional[int] = None