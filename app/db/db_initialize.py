from app.db.database import SessionLocal
from app.db.models import Game, User


def initialize_database():
    db = SessionLocal()
    try:

        predefined_games = [
            Game(
                title="The Legend of Zelda: Tears of the Kingdom",
                description="The Legend of Zelda: Tears of the Kingdom is the sequel to The Legend of Zelda: Breath of the Wild. The setting for Link’s adventure has been expanded to include the skies above the vast lands of Hyrule.",
                details="Genres: Role-playing (RPG), Adventure, Action, Fantasy, Sci-Fi, Open world\n"
                    "Game mode: Single player\n"
                    "Developer: Nintendo EPD Production Group No.3\n"
                    "Publisher: Nintendo",
                releases="Nintendo Switch: 2023-5-12"
            ),Game(
                title="Tunic",
                description="Tunic is an action adventure about a tiny fox in a big world. Explore the wilderness, discover spooky ruins, and fight terrible creatures from long ago.",
                details="Genres: Puzzle, Role-playing (RPG), Adventure, Indie, Action, Fantasy\n"
                    "Game mode: Single player\n"
                    "Developer: Andrew Shouldice\n"
                    "Publisher: Finji",
                releases="Windows: 2022-3-16\n"
                    "Mac: 2022-3-16\n"
                    "Xbox One: 2022-3-16\n"
                    "Xbox Series X|S: 2022-3-16\n"
                    "PlayStation 4: 2022-9-27\n"
                    "PlayStation 5: 2022-9-27\n"
                    "Nintendo Switch: 2022-9-27"
            ),Game(
                title="Sekiro",
                description="Enter a dark and brutal new gameplay experience from the creators of Bloodborne and the Dark Souls series. Sekiro: Shadows Die Twice is an intense, third-person, action-adventure set against the bloody backdrop of 14th-century Japan. Step into the role of a disgraced warrior brought back from the brink of death whose mission is to rescue his master and exact revenge on his arch nemesis.",
                details="Genres: Adventure, Action, Fantasy, Stealth\n"
                    "Game mode: Single player\n"
                    "Developer: FromSoftware\n"
                    "Publisher: Activision",
                releases="Windows: 2019-3-22\n"
                    "PlayStation 4: 2019-3-22\n"
                    "Xbox One: 2019-3-22"
            )
        ]

        with open("app/images/zelda_totk.png", "rb") as file:
            predefined_games[0].image = file.read()

        with open("app/images/tunic.png", "rb") as file:
            predefined_games[1].image = file.read()

        with open("app/images/sekiro.png", "rb") as file:
            predefined_games[2].image = file.read()

        for game in predefined_games:
            if not db.query(Game).filter(Game.title == game.title).first():
                db.add(game)

        user = User(username= "test", password= "test")
        if not db.query(User).filter(User.username == user.username).first():
            db.add(user)

        db.commit()
    finally:
        db.close()
