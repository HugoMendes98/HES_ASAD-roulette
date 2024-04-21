
from flask import request, current_app
from . import roulette_logic_blueprint

GAME_PATH = "/games/1"

the_game = {"type": "bid-able", "bids": []}

@roulette_logic_blueprint.post("/<game_id>/bet")
def add_bet(game_id):
    # request json:
    # "position_id":
    # "value" signed integer
    global the_game

    if game_id != "1":
        return "NotFound", 404

    # TODO: validate input
    if the_game["type"] != "bid-able":
        return "NotPlayable", 422
    # user.bet(game_id, inout_bets.enum, wager)
    # IDK if the_game["bids"] is automatically updated
    # the_game = {**the_game, "bids": [*the_game["bids"], request.json]}
    
    #1 broacast game status
    
    current_app.socketio_instance.emit(GAME_PATH, the_game)
    return {}, 201

def get_game_satus():
    pass

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