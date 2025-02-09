from datetime import timedelta
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.db.models import User
from app.security.jwt_util import get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token

router = APIRouter(
    prefix="/user",
    tags=["Users"]
)

# Función para probar el token
@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    print(current_user.idUser)
    print(current_user.username)
    print(current_user.password)
    return UserResponse(
        idUser=current_user.idUser,
        username=current_user.username,
        password=current_user.password,
    )

@router.post("/login")
def get_user(form_data: OAuth2PasswordRequestForm = Depends(), db:Session=Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if form_data.password != user.password:
        raise HTTPException(status_code=401, detail="Wrong credentials")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {
        "idUser": user.idUser,
        "token": f"Bearer {access_token}",
        "token_type": "bearer"}

@router.post("/insert")
def insert_user(user: UserCreate, db:Session=Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = User(
        username = user.username,
        password = user.password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

    return {"idUser": new_user.idUser, "token": f"Bearer {access_token}", "token_type": "bearer"}
