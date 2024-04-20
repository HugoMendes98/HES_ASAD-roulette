import pytest
from backend.src.models import db, User, Game, Bid
from backend.src.app import create_app

@pytest.fixture
def client():
    app,_ = create_app()
    app.testing = True
    with app.test_client() as testclient:
        with app.app_context():
            db.create_all()
            yield testclient

def test_create_meta(client):
    m = User(username='molasse')
    db.session.add(m)
    db.session.commit()
    #res = client.get(f'/meta/{m.id}')
    assert m.username == "molasse"