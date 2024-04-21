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
    m = User.new(username='molasse')
    assert m.username == "molasse"

#def new(cls, wager, inOutbet: InOutBets, user, round):
def test_bid_update(client):
    g = Game.new()
    u = User.new(password_hash="asdkdlj",username="Jean Test")
    r = Round.new(round_number=1, game=g)
    b = Bid.new(inOutbet=InOutBets.FIFTEEN, wager=10, user=u, round=r)

def test_bid(client):
    User.new(username='oly')
    r = client.post("/games/1/bet", data=json.dumps(dict(position_id='1', value=5, username="oly")), content_type='application/json')
    assert r.status_code == 201
