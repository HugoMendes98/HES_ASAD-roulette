from flask import Blueprint, current_app, request
from flask_jwt_extended import jwt_required
from flask_socketio import SocketIO

from ..models import Game
from ..models.round_info import InOutBets
from ..sockets import get_game_socket_path
from .auth_utils import get_current_user
from .common import API_PREFIX

game_blueprint = Blueprint("game", __name__, url_prefix=API_PREFIX + "/games")


@game_blueprint.post("/<game_id>/bet")
@jwt_required()
def add_bet(game_id):
	# request json:
	# "position_id":
	# "value" signed integer

	user = get_current_user()

	r = request.json
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
		}, 201
	else:
		return {"balance": user.balance}, 201
