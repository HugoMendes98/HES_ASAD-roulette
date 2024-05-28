from datetime import datetime

from flask_socketio import SocketIO

# from . import config
from .models import Game
from .sockets import get_game_socket_path, register_sockets


def event_loop(app, game_id=1):
    with app.app_context():
        socketio: SocketIO = app.socketio_instance

        # Wait potential socket connections
        socketio.sleep(2)

        current_game = Game.get(game_id)

        current_game.init_game()

        register_sockets(socketio)

        print("Game is about to start")

        while True:
            current_round = current_game.get_last_round()
            next_state = current_round.next_state_timestamp
            sleep_time = (next_state - datetime.utcnow()).total_seconds()

            state = current_round.to_json()
            print("Emit game state:", state)

            app.socketio_instance.emit(get_game_socket_path(current_game), state)

            print("Sleep (s):", sleep_time)
            socketio.sleep(sleep_time)

            current_game.state_machine()

