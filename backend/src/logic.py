
from flask import request, current_app, jsonify
from . import roulette_logic_blueprint
from .models import User, InOutBets

GAME_PATH = "/games/1"


@roulette_logic_blueprint.post("/<game_id>/bet")
def add_bet(game_id):
    # request json:
    # "position_id":
    # "value" signed integer
    global the_game

    if game_id != "1":
        return "NotFound", 404
    
    r = request.json
    username = r["username"]
    try:
        bid = User.get(username).bet(InOutBets(r["position_id"]), r["value"], 1)
    except Exception as exc:
        print("add_bet route: exception occured:", exc)
        return "error", 422

    # TODO: broacast game status
    
    current_app.socketio_instance.emit(GAME_PATH, the_game)
    return {}, 201

@roulette_logic_blueprint.get("/<game_id>/status")
def get_game_satus():
    return jsonify({})

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
        
        # Cannot bid, send result
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