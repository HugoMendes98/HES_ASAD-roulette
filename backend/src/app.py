import os

from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

from .logic import event_loop, roulette_logic_blueprint
from .models import register_models
from .routes import roulette_website_blueprint


def create_app():
	app = Flask(__name__)
	app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
		"DATABASE_URI", "sqlite://"
	)
	register_models(app)
	app.register_blueprint(roulette_logic_blueprint)
	app.register_blueprint(roulette_website_blueprint)

	CORS(app, origins="*")
	app.socketio_instance = SocketIO(app, cors_allowed_origins="*", logger=True)
	return app


def main():
	app = create_app()

	socketio = app.socketio_instance
	socketio.start_background_task(event_loop, app)
	socketio.run(
		app,
		host=os.environ.get("APP_HOST", "localhost"),
		port=int(os.environ.get("APP_PORT", "5000")),
	)


if __name__ == "__main__":
	main()
