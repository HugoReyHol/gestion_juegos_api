from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.db.models import User

router = APIRouter(
    prefix="/user",
    tags=["Users"]
)

@router.get("/{username}", response_model=UserResponse)
def get_user(username: str, db:Session=Depends(get_db)) -> dict:
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

@router.post("/")
def insert_user(user: UserCreate, db:Session=Depends(get_db)) -> dict:
    # TODO comprobar que no cree usuarios con el mismo username
    # TODO comprobar si devuelve el idUser para asignarlo en el cliente
    existing_user = db.query(User).filter(User.userGame == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = User(
        username = user.username,
        password = user.password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user.idUser

