from datetime import timedelta
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.user import UserRequest, UserResponse
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

@router.post("/login", responses={
    404: {
        "description": "User not found",
        "content": {
            "application/json": {
                "example": {"detail": "string"}
            }
        }
    },
    401: {
        "description": "Wrong credentials",
        "content": {
            "application/json": {
                "example": {"detail": "string"}
            }
        }
    }
})
def get_user(user_req: UserRequest, db:Session=Depends(get_db)):
    user = db.query(User).filter(User.username == user_req.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user_req.password != user.password:
        raise HTTPException(status_code=401, detail="Wrong credentials")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {
        "idUser": user.idUser,
        "username": user.username,
        "password": user.password,
        "token": f"Bearer {access_token}",
    }

@router.post("/insert", response_model=UserResponse, responses={
    400: {
        "description": "The user already exists",
        "content": {
            "application/json": {
                "example": {"detail": "string"}
            }
        }
    }
})
def insert_user(user_req: UserRequest, db:Session=Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user_req.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="The user already exists")

    new_user = User(
        username = user_req.username,
        password = user_req.password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user_req.username}, expires_delta=access_token_expires)

    return {
        "idUser": new_user.idUser,
        "username": new_user.username,
        "password": new_user.password,
        "token": f"Bearer {access_token}"
    }
