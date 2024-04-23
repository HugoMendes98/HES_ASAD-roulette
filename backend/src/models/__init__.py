from .bid import Bid
from .db import db
from .game import Game
from .round import Round
from .user import User


def configure_database(app):
	with app.app_context():
		db.create_all()
		if Game.get(1) is None:
			Game.new(1)


def register_models(app):
	db.init_app(app)
	configure_database(app)
