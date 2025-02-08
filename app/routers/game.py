from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import models
from app.db.database import get_db
from app.schemas.game import GameResponse

router = APIRouter(
    prefix="/game",
    tags=["Games"]
)

@router.get("/", response_model=List[GameResponse])
def get_games(db:Session=Depends(get_db)):
    games = db.query(models.Game).all
    return games