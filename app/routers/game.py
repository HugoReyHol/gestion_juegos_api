from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy import asc
from sqlalchemy.orm import Session
from app.db.models import Game
from app.db.database import get_db
from app.schemas.game import GameResponse

router = APIRouter(
    prefix="/game",
    tags=["Games"]
)

@router.get("/", response_model=List[GameResponse])
def get_games(db:Session=Depends(get_db)) -> List[GameResponse]:
    games = db.query(Game).order_by(asc(Game.title)).all()
    return [GameResponse.from_game_model(game) for game in games]