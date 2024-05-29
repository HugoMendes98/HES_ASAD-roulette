import os

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO

from . import config
from .logic import event_loop
from .models import Game, register_models
from .routes.auth import auth_blueprint
from .routes.game import game_blueprint


def create_app():
	app = Flask(__name__)

	app.config["JWT_SECRET_KEY"] = os.environ.get("APP_SECRET", "super-secret")
	app.config["JWT_ACCESS_TOKEN_EXPIRES"] = config.AUTH_JWT_DURATION

	app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
		"DATABASE_URI", "sqlite://"
	)

	register_models(app)
	app.register_blueprint(auth_blueprint)
	app.register_blueprint(game_blueprint)

	CORS(app, origins="*")
	app.socketio_instance = socketio = SocketIO(
		app, cors_allowed_origins="*", logger=True
	)

	with app.app_context():
		for i in range(1, 4):
			if Game.get(i) is None:
				Game.new(i)
			socketio.start_background_task(event_loop, app, i)

	JWTManager(app)
	return app


def main():
	app = create_app()
	app.socketio_instance.run(
		app,
		host=os.environ.get("APP_HOST", "localhost"),
		port=int(os.environ.get("APP_PORT", "5000")),
	)


if __name__ == "__main__":
	main()
