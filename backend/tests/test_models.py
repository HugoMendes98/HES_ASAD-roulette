import json
import pytest
from backend.src.models import db, User, Game, Bid, Round, RoundStates, InOutBets, Slots
from backend.src.app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    with app.test_client() as testclient:
        with app.app_context():
            db.create_all()
            yield testclient


def test_users(client):
    m = User.new(username="molasse")
    assert m.username == "molasse"


def test_bid_wager_update(client):
    g = Game.new()
    u = User.new(password_hash="asdkdlj", username="Jean Test")
    r = Round.new(round_number=1, game=g)
    b = Bid.new(inOutbet=InOutBets.FIFTEEN, wager=10, user=u, round=r)
    Bid.update_wager(b.id, 20)
    assert b.wager == 20


def test_payout_full(client):
    g = Game.new()
    u_1 = User.new(password_hash="asdkdlj", username="Jean Test")
    u_2 = User.new(password_hash="asdkdlj", username="Test Andy")
    # ---------------------------------------
    g.go_to_idle()

    assert not u_1.bids

    r = g.get_last_round()
    assert r.round_number == 1
    assert r.state == RoundStates.IDLE.value[1]
    ts = r.timestamp
    assert ts  # is not none ?
    assert r.game_id == g.id
    assert not r.winning_slot
    assert not r.get_winning_bids()

    with pytest.raises(Exception):
        u_1.bet(game=g, player_bet=InOutBets.ELEVEN, wager=10)

    # --------------------------------------
    g.go_to_bidable()

    assert u_1.bet(game=g, player_bet=InOutBets.ELEVEN, wager=10)
    assert u_2.bet(game=g, player_bet=InOutBets.TWELVE, wager=30)

    assert u_1.balance == 190
    assert u_2.balance == 170

    assert len(u_2.bids) == 1

    b_1 : Bid = Bid.get_bids_from_user_and_round_with_bet(
        user=u_1, round=r, player_bet=InOutBets.ELEVEN
    )
    b_2 : Bid = Bid.get_bids_from_user_and_round_with_bet(
        user=u_2, round=r, player_bet=InOutBets.TWELVE
    )

    assert not b_2.is_won
    assert b_2.wager == 30

    assert u_2.bet(game=g, player_bet=InOutBets.TWELVE, wager=-20)
    assert u_2.balance == 190
    assert b_2.wager == 10


    with pytest.raises(Exception):
        u_1.bet(game=g, player_bet=InOutBets.ELEVEN, wager=10000)

    r = g.get_last_round()
    assert r.round_number == 1
    assert r.state == RoundStates.BIDABLE.value[1]
    assert ts == r.timestamp
    assert r.game_id == g.id
    assert not r.winning_slot
    assert not r.get_winning_bids()

    #------------------------------
    g.go_to_waiting()

    r = g.get_last_round()
    assert r.round_number == 1
    assert r.state == RoundStates.WAITING.value[1]
    assert ts == r.timestamp
    assert r.game_id == g.id
    assert not r.winning_slot
    assert not r.get_winning_bids()

    with pytest.raises(Exception):
        u_1.bet(game=g, player_bet=InOutBets.ELEVEN, wager=10)

    #-----------------------------
    g.go_to_result(Slots.ELEVEN)

    r = g.get_last_round()
    assert r.round_number == 1
    assert r.state == RoundStates.RESULT.value[1]
    assert ts == r.timestamp
    assert r.game_id == g.id
    assert r.winning_slot == Slots.ELEVEN.value
    w_b = r.get_winning_bids()
    assert(len(w_b)==1)
    assert(w_b[0].is_won)


def test_bid(client):


    User.new(username="oly")
    g = Game.get(1)
    g.go_to_idle()
    g.go_to_bidable()
    r = client.post(
        "/games/1/bet",
        data=json.dumps(dict(position_id=1, value=5, username="oly")),
        content_type="application/json",
    )
    assert r.status_code == 201