from flask import Blueprint, current_app, request
from flask_socketio import SocketIO

from ..models import Game, User
from ..models.round_info import InOutBets
from ..sockets import get_game_socket_path
from .common import API_PREFIX

game_blueprint = Blueprint("game", __name__, url_prefix=API_PREFIX + "/games")


@game_blueprint.post("/<game_id>/bet")
def add_bet(game_id):
	# TODO: get user from auth

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
		print("add_bet route: exception occurred:", exc)
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
		return {"balance": user.balance}, 201
