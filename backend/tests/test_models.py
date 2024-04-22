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
    u = User.new(password_hash="asdkdlj", username="Jean Test")
    u = User.new(password_hash="asdkdlj", username="Test Andy")
    test_r = g.go_to_idle()

    print(test_r)

    r = g.get_last_round()
    assert r.round_number == 1
    assert r.state == RoundStates.IDLE.value[1]
    print(r.timestamp)
    assert r.timestamp  # is not none ?
    assert r.game_id == g.id
    assert not r.winning_slot
    assert not r.get_winning_bids()

    # b = Bid.new(inOutbet=InOutBets.FIFTEEN, wager=10, user=u, round=r)


def test_bid(client):
    User.new(username="oly")
    r = client.post(
        "/games/1/bet",
        data=json.dumps(dict(position_id="1", value=5, username="oly")),
        content_type="application/json",
    )
    assert r.status_code == 201
