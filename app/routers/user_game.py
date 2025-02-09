from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import UserGame, User
from app.schemas.user_game import UserGameUpdate, UserGameScheme
from app.security.jwt_util import get_current_user

router = APIRouter(
    prefix="/user_game",
    tags=["UserGames"]
)

@router.post("/")
def insert_user_game(user_game: UserGameScheme, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_user_game = UserGame(idUser=current_user.idUser, **user_game.model_dump(exclude_unset=True))
    db.add(new_user_game)
    db.commit()
    db.refresh(new_user_game)

@router.get("/", response_model=List[UserGameScheme])
def get_user_games(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> List[UserGameScheme]:
    user_games = db.query(UserGame).filter(UserGame.idUser == current_user.idUser).all()
    return user_games

@router.patch("/{idGame}")
def update_user_game(id_game: int, updates: UserGameUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_game = db.query(UserGame).filter(UserGame.idUser == current_user.idUser, UserGame.idGame == id_game)
    if not user_game.first():
        raise HTTPException(status_code=404, detail="UserGame not found")
    user_game.update(updates.model_dump(exclude_unset=True))
    db.commit()

@router.delete("/{idGame}")
def delete_user_game(id_game: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_game = db.query(UserGame).filter(UserGame.idUser == current_user.idUser, UserGame.idGame == id_game).first()
    if not user_game:
        raise HTTPException(status_code=404, detail="UserGame not found")
    db.delete(user_game)
    db.commit()


