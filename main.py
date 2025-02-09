from fastapi import FastAPI
import uvicorn
from app.db.db_initialize import initialize_database
from app.routers import user, game, user_game
from app.db.database import Base, engine

def create_tables():
    Base.metadata.create_all(bind=engine)

create_tables()
initialize_database()

app: FastAPI = FastAPI()
app.include_router(user.router)
app.include_router(game.router)
app.include_router(user_game.router)

if __name__ == '__main__':
    uvicorn.run("main:app", port=8000, reload=True)