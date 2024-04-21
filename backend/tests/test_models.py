import json
import pytest
from backend.src.models import db, User, Game, Bid
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

    

def test_bid(client):
    User.new(username='oly')
    r = client.post("/games/1/bet", data=json.dumps(dict(position_id='1', value=5, username="oly")), content_type='application/json')
    assert r.status_code == 201