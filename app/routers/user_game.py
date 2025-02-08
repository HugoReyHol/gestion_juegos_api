from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import UserGame
from app.schemas.user_game import UserGameUpdate, UserGameScheme

router = APIRouter(
    prefix="/user_game",
    tags=["UserGames"]
)

@router.post("/", response_model=bool)
def insert_user_game(user_game: UserGameScheme, db: Session = Depends(get_db)) -> bool:
    new_user_game = UserGame(**user_game.model_dump())
    db.add(new_user_game)
    db.commit()
    db.refresh(new_user_game)
    return True

@router.get("/{idUser}", response_model=List[UserGameScheme])
def get_user_games(id_user: int, db: Session = Depends(get_db)) -> List[UserGameScheme]:
    user_games = db.query(UserGame).filter(UserGame.idUser == id_user).all()
    return user_games

@router.patch("/{idUser}/{idGame}", response_model=bool)
def update_user_game(id_user: int, id_game: int, updates: UserGameUpdate, db: Session = Depends(get_db)) -> bool:
    user_game = db.query(UserGame).filter(UserGame.idUser == id_user, UserGame.idGame == id_game).first()
    if not user_game:
        raise HTTPException(status_code=404, detail="UserGame not found")
    # for key, value in updates.model_dump(exclude_unset=True).items():
    #     setattr(user_game, key, value)
    user_game.update(updates.model_dump(exclude_unset=True))
    db.commit()
    return True

@router.delete("/{idUser}/{idGame}", response_model=bool)
def delete_user_game(id_user: int, id_game: int, db: Session = Depends(get_db)) -> bool:
    user_game = db.query(UserGame).filter(UserGame.idUser == id_user, UserGame.idGame == id_game).first()
    if not user_game:
        raise HTTPException(status_code=404, detail="UserGame not found")
    db.delete(user_game)
    db.commit()
    return True



