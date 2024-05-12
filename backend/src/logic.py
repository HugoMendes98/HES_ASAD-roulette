from datetime import datetime, timedelta
from random import randint

from flask_socketio import SocketIO

from . import config
from .models import Game
from .models.round_info import RoundStates, Slots
from .sockets import get_game_socket_path, register_sockets


def event_loop(app):
	with app.app_context():
		socketio: SocketIO = app.socketio_instance

		# Wait potential socket connections
		socketio.sleep(2)

		current_game = Game.get(1)
		current_game.go_to_idle(
			datetime.utcnow() + timedelta(seconds=config.IDLE_time_s)
		)

		register_sockets(socketio)

		print("Game is about to start")

		while True:
			current_round = current_game.get_last_round()
			next_state = current_round.next_state_timestamp
			sleep_time = (next_state - datetime.utcnow()).total_seconds()

			state = current_round.to_json()
			print("Emit game state:", state)

			app.socketio_instance.emit(
				get_game_socket_path(current_game), state
			)

			print("Sleep (s):", sleep_time)
			socketio.sleep(sleep_time)

			# Get updated last round (with bets)
			current_round = current_game.get_last_round()

			# "State machine"
			if RoundStates(current_round.state) == RoundStates.IDLE:
				current_game.go_to_bidable(
					datetime.utcnow() + timedelta(seconds=config.BIDABLE_time_s)
				)
				print("La manche est en préparation")
			elif RoundStates(current_round.state) == RoundStates.BIDABLE:
				current_game.go_to_waiting(
					datetime.utcnow() + timedelta(seconds=config.WAITING_time_s)
				)
				print(
					"Les paris sont fermés, les résultats sera annoncé dans quelque temps"
				)
			elif RoundStates(current_round.state) == RoundStates.WAITING:
				current_game.go_to_result(
					Slots(randint(0, 36)),
					datetime.utcnow()
					+ timedelta(seconds=config.RESULTS_time_s),
				)
				print("Les résultats sont tombés")
			elif RoundStates(current_round.state) == RoundStates.RESULT:
				current_game.go_to_idle(
					datetime.utcnow() + timedelta(seconds=config.IDLE_time_s)
				)
				print(
					"La manche est terminée, un nouveau round va bientot commencer..."
				)
