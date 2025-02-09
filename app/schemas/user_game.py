from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class UserGameInsert(BaseModel):
    idGame: int
    score: Optional[int]
    timePlayed: int
    gameState: str
    lastChange: datetime

class UserGameResponse(BaseModel):
    idUser: int
    idGame: int
    score: Optional[int]
    timePlayed: int
    gameState: str
    lastChange: int

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def convert_timestamp(cls, user_game):
        return cls.model_validate({
            "idUser": user_game.idUser,
            "idGame": user_game.idGame,
            "score": user_game.score,
            "timePlayed": user_game.timePlayed,
            "gameState": user_game.gameState,
            "lastChange": int(user_game.lastChange.timestamp() * 1000)
        })

class UserGameUpdate(BaseModel):
    score: Optional[int] = None
    timePlayed: Optional[int] = None
    gameState: Optional[str] = None
    lastChange: Optional[datetime] = None