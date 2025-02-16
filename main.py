from fastapi import FastAPI, Request
import uvicorn
from app.db.db_initialize import initialize_database
from app.routers import user, game, user_game
from app.db.database import Base, engine

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

def create_tables():
    Base.metadata.create_all(bind=engine)

create_tables()
initialize_database()

app: FastAPI = FastAPI()
app.include_router(user.router)
app.include_router(game.router)
app.include_router(user_game.router)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    j = JSONResponse(
        status_code=422,
        content={"error": "Error de validación", "details": exc.errors(), "body": exc.body},
    )

    print(j.body)

    return j

if __name__ == '__main__':
    uvicorn.run("main:app", port=8000, reload=True)