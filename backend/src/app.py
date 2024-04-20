import random


from flask import Flask, request
from flask_cors import CORS
from flask_socketio import SocketIO

from .models import register_models

# The "only" game (demo/test purpose)
the_game = {"type": "idle", "round": 0}

def create_app():
    app = Flask(__name__)
    app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    register_models(app)

    CORS(app, origins="*")
    socketio = SocketIO(app, cors_allowed_origins="*", logger=True)
    return app, socketio

def main():
    # init db
    
    app, socketio = create_app()

    

    socketio.start_background_task(event_loop, socketio)
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)

if __name__ == "__main__":
    main()
