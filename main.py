from fastapi import FastAPI
import uvicorn
from fastapi.openapi.utils import get_openapi

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


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="My API",
        version="1.0.0",
        routes=app.routes,
    )

    # Añadir el esquema de seguridad JWT a la documentación
    openapi_schema["components"]["securitySchemes"] = {
        "Bearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Ingresa el token JWT en el formato: **Bearer <token>**"
        }
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

if __name__ == '__main__':
    uvicorn.run("main:app", port=8000, reload=True)