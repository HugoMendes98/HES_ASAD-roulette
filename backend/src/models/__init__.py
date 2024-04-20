from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .bid import Bid
from .game import Game
from .user import User


from enum import Enum



def register_models(app):
    db.init_app(app)

class GameType(Enum):
    BIDABLE = "bid-able", 0
    IDLE = "idle", 1
    WAITING = "waiting", 2
    RESULT = "results", 3