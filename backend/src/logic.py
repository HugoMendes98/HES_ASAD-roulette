
from random import randint
from datetime import datetime, timedelta
from flask import request, current_app, jsonify
from . import roulette_logic_blueprint
from .models import User, InOutBets, Game, RoundStates

GAME_PATH = "/games/1"
BIDABLE_time_s = 30
IDLE_time_s = 5
WAITING_time_s = 5
RESULTS_time_s = 5


@roulette_logic_blueprint.post("/<game_id>/bet")
def add_bet(game_id):
    # request json:
    # "position_id":
    # "value" signed integer
    
    if game_id != "1":
        return "NotFound", 404
    
    game_one = Game.get(int(game_id))
    
    r = request.json
    user = User.get(r["username"])
    try:
        bid = user.bet(InOutBets(r["position_id"]), r["value"], game_one)
    except Exception as exc:
        print("add_bet route: exception occured:", exc)
        return f"error: {exc}", 422

    current_round = game_one.get_last_round()

    current_app.socketio_instance.emit(GAME_PATH, current_round.to_dict())
    if bid is not None:
        return {"value": int(bid.wager), "position_id": bid.inOutbet, "balance": user.balance}, 201
    else:
        return {}, 201

@roulette_logic_blueprint.get("/<game_id>/status")
def get_game_satus(game_id):
    if game_id != "1":
        return "NotFound", 404
    current_round = Game.get(int(game_id)).get_last_round()
    return jsonify(current_round.to_dict())

def event_loop(socketio):
    with current_app.app_context():
        current_game = Game.get(1)
        current_game.go_to_idle()

        # Wait potential socket connections
        socketio.sleep(5)
        print("Game is about to start")

        wining_slot = None
        pay_out = None

        while True:
            current_round = current_game.get_last_round()
            if RoundStates(current_round.state) == RoundStates.IDLE:
                if (current_round.next_state_timestamp - datetime.utcnow()) < 0:
                    print("Les paris sont ouverts")
                    wining_slot = None
                    pay_out = None
                    current_game.go_to_bidable(datetime.utcnow() + timedelta(seconds=BIDABLE_time_s))
            elif RoundStates(current_round.state) == RoundStates.BIDABLE:
                if (current_round.next_state_timestamp - datetime.utcnow()) < 0:
                    current_game.go_to_waiting(datetime.utcnow() + timedelta(seconds=WAITING_time_s))
                    wining_slot = randint(0, 36)
                    pay_out = None
                    print("Les paris sont fermés, les résultats sera annoncé dans quelque temps")
            elif RoundStates(current_round.state) == RoundStates.WAITING:
                if (current_round.next_state_timestamp - datetime.utcnow()) < 0:
                    current_game.go_to_result(wining_slot, datetime.utcnow() + timedelta(seconds=WAITING_time_s))
                    current_round = current_game.get_last_round()
                    pay_out = current_round.pay_out()
                    print("Les résultats sont tombés. wining_slot",wining_slot, "results:",pay_out)
            elif RoundStates(current_round.state) == RoundStates.RESULT:
                if (current_round.next_state_timestamp - datetime.utcnow()) < 0:
                    wining_slot = None
                    pay_out = None
                    current_game.go_to_idle(datetime.utcnow() + timedelta(seconds=IDLE_time_s))
                    print("La manche est terminée, un nouveau round va bientot commencer...")

            state = current_game.get_last_round().to_dict()
            state["wining_slot"] = wining_slot
            state["pay_out"] = pay_out
            socketio.emit(GAME_PATH, state)
            print("Emit game state:", state)
            socketio.sleep(1)