import os

from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

from .logic import event_loop
from .models import register_models
from .routes.auth import auth_blueprint
from .routes.game import game_blueprint


def create_app():
	app = Flask(__name__)
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
	socketio.start_background_task(event_loop, app)

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
