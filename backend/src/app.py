import random

from flask import Flask, request
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

# init db
app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../../roulette.db'
db = SQLAlchemy(app)

# need to import after db init to avoid circular imports
from models.game import Game
from models.user import User


CORS(app, origins="*")
socketio = SocketIO(app, cors_allowed_origins="*", logger=True)



# The "only" game (demo/test purpose)
the_game = {"type": "idle", "round": 0}
GAME_PATH = "/games/1"


@app.post("/games/<game_id>/bet")
def add_bet(game_id):
	if game_id != "1":
		return "NotFound", 404

	global the_game

	# TODO: validate input
	if the_game["type"] != "bid-able":
		return "NotPlayable", 422

	the_game = {**the_game, "bids": [*the_game["bids"], request.json]}
	socketio.emit(GAME_PATH, the_game)
	return {}, 201


def event_loop():
	# TODO: to remove -> Run async loops for auto-managed games
	global the_game

	# Wait potential socket connections
	socketio.sleep(5)

	time = 5

	# (demo/test purpose)
	while True:
		socketio.emit(GAME_PATH, the_game)
		socketio.sleep(time)

		# Can bid
		the_game = {
			"type": "bid-able",
			"bids": [],
			"round": the_game["round"] + 1,
		}
		socketio.emit(GAME_PATH, the_game)
		socketio.sleep(time)

		# Cannot bid, but no result yet
		the_game = {**the_game, "type": "waiting"}
		socketio.emit(GAME_PATH, the_game)
		socketio.sleep(time)

		# Results are returned
		the_game = {
			**the_game,
			"type": "results",
			"result": random.randint(0, 40),
		}
		socketio.emit(GAME_PATH, the_game)
		socketio.sleep(time)

		# "reset" for next round
		the_game = {"type": "idle", "round": the_game["round"]}


if __name__ == "__main__":
	socketio.start_background_task(event_loop)
	socketio.run(app, host="0.0.0.0", port=5000, debug=True)
