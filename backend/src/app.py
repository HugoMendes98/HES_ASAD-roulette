import random


from flask import Flask, request
from flask_cors import CORS
from flask_socketio import SocketIO
from threading import Event

from .models import register_models
from .logic import event_loop, roulette_logic_blueprint
from .routes import roulette_website_blueprint

# The "only" game (demo/test purpose)
the_game = {"type": "idle", "round": 0}

def create_app():
    app = Flask(__name__)
    app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
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
    socketio.run(app, host="localhost", port=5000)

if __name__ == "__main__":
    main()
