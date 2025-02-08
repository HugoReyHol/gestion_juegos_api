from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.db.models import User
from app.security.jwt_util import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, hash_password, verify_password

router = APIRouter(
    prefix="/user",
    tags=["Users"]
)

@router.post("/login")
def get_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db:Session=Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(plain_password=form_data.password, hashed_password=user.password):
        raise HTTPException(status_code=401, detail="Wrong credentials")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/insert")
def insert_user(user: UserCreate, db:Session=Depends(get_db)) -> int:
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = User(
        username = user.username,
        password = hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user.idUser

