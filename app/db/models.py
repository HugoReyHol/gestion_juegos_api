from app.db.database import Base
from sqlalchemy import Column,Integer,String, LargeBinary
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "Users"
    idUser = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    password = Column(String)
    userGame = relationship("UserGame", backref="Users", cascade="delete,merge")


class Game(Base):
    __tablename__ = "Games"
    idGame = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    description = Column(String)
    image = Column(LargeBinary)
    details = Column(String)
    releases = Column(String)
    userGame = relationship("UserGame", backref="Games", cascade="delete,merge")

class UserGame(Base):
    __tablename__ = "User_Games"
    idGame = Column(Integer, ForeignKey("Games.idGame", ondelete="CASCADE"), primary_key=True)
    idUser = Column(Integer, ForeignKey("Users.idUser", ondelete="CASCADE"), primary_key=True)
    score = Column(Integer, nullable=True)
    timePlayed = Column(Integer)
    gameState = Column(String)
    lastChange = Column(Integer)

