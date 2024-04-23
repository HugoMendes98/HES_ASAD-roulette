from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

from . import roulette_logic_blueprint, roulette_website_blueprint
from .models import register_models
from .routes import register_routes


def create_app():
	app = Flask(__name__)
	app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

	register_models(app)
	register_routes()

	app.register_blueprint(roulette_logic_blueprint)
	app.register_blueprint(roulette_website_blueprint)

	CORS(app, origins="*")

	return app, SocketIO(app, cors_allowed_origins="*", logger=True)


def main():
	app, socketio = create_app()

	# socketio.start_background_task(event_loop, app)
	socketio.run(app, host="localhost", port=5000)


if __name__ == "__main__":
	main()
