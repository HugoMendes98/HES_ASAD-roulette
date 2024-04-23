from flask_socketio import SocketIO
from flask_socketio import emit as socket_emit

from .models import Game


def get_game_socket_path(game: Game):
	return "/games/{}".format(game.id)


def register_sockets(socketio: SocketIO):
	@socketio.on("/games/refresh")
	def refresh_game(data):
		"""
		A socket event that asks to refresh the default emit data
		so "call" to this event with `{gameId: <number>}` will then emit `/games/1` event to the client that requested the refresh
		"""

		# In case of error (no existing game), simply ignore
		if "gameId" not in data:
			return

		game = Game.get(data["gameId"])
		if game is None:
			return

		round = game.get_last_round()
		if round is None:
			return

		# Emit only to the one asking the data
		socket_emit(
			get_game_socket_path(game), round.to_json(), broadcast=False
		)
