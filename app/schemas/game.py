import base64
from pydantic import BaseModel, ConfigDict

class GameResponse(BaseModel):
    idGame: int
    title: str
    description: str
    image: str
    details: str
    releases: str

    model_config = ConfigDict(from_attributes=True)

    # Convierte la imagen binaria a texto plano
    @classmethod
    def from_game_model(cls, game):
        image_base64 = base64.b64encode(game.image).decode("utf-8")
        return cls.model_validate({
            "idGame": game.idGame,
            "title": game.title,
            "description": game.description,
            "image": image_base64,
            "details": game.details,
            "releases": game.releases,
        })