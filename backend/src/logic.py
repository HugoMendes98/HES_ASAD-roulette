
from flask import request
from . import roulette_logic_blueprint

GAME_PATH = "/games/1"

the_game = {}

@roulette_logic_blueprint.post("/games/<game_id>/bet")
def add_bet(game_id):
    if game_id != "1":
        return "NotFound", 404

    # TODO: validate input
    if the_game["type"] != "bid-able":
        return "NotPlayable", 422

    # IDK if the_game["bids"] is automatically updated
    the_game = {**the_game, "bids": [*the_game["bids"], request.json]}
    socketio.emit(GAME_PATH, the_game)
    return {}, 201


def event_loop(socketio):
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