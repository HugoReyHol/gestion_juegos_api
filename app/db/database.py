from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.db.models import Game

SQLALCHEMY_DATABASE_URL = "postgresql://odoo:odoo@localhost:5342/gestion_juegos"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine,autocommit=False,autoflush=False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def initialize_database():
    db = SessionLocal()
    try:
        predefined_games = [
            Game(title="Game 1", description="Description 1", image=b"", details="Details 1", releases="2025-01-01"),
            Game(title="Game 2", description="Description 2", image=b"", details="Details 2", releases="2025-02-01"),
            Game(title="Game 3", description="Description 3", image=b"", details="Details 3", releases="2025-03-01")
        ]

        for game in predefined_games:
            if not db.query(Game).filter(Game.title == game.title).first():
                db.add(game)

        db.commit()
    finally:
        db.close()


initialize_database()