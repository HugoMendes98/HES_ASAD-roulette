from datetime import datetime, timedelta
from random import randint

from flask import current_app, request
from flask_socketio import SocketIO

from . import config, roulette_logic_blueprint
from .models import Game, User
from .models.round_info import InOutBets, RoundStates, Slots
from .sockets import get_game_socket_path, register_sockets


@roulette_logic_blueprint.post("/<game_id>/bet")
def add_bet(game_id):
	# request json:
	# "position_id":
	# "value" signed integer

	r = request.json
	user = User.get(r["username"])
	if user is None:
		return "Forbidden", 401

	game = Game.get(int(game_id))
	if game is None:
		return "NotFound", 404

	try:
		bid = user.bet(InOutBets(r["position_id"]), r["value"], game)
	except Exception as exc:
		print("add_bet route: exception occured:", exc)
		return f"error: {exc}", 422

	current_round = game.get_last_round()

	socketio: SocketIO = current_app.socketio_instance
	socketio.emit(get_game_socket_path(game), current_round.to_json())

	if bid is not None:
		return {
			"value": int(bid.wager),
			"position_id": bid.inOutbet,
			"balance": user.balance,
		}, 201
	else:
		return {}, 201


@roulette_logic_blueprint.get("/<game_id>/status")
def get_game_satus(game_id):
	game = Game.get(int(game_id))
	if game is None:
		return "NotFound", 404

	return game.get_last_round().to_json()


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
