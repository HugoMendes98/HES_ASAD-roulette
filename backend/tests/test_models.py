import json

import pytest

from src.app import create_app
from src.models import (
	Bid,
	Game,
	Round,
	User,
	db,
)
from src.models.round_info import (
	InOutBets,
	RoundStates,
	Slots,
)


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


def test_perfect_bid_removal(client):
	g = Game.new()
	u = User.new(password_hash="asdkdlj", username="Jean Zero")
	g.go_to_idle()
	g.go_to_bidable()

	assert u.balance == 200

	b_1 = u.bet(game=g, player_bet=InOutBets.TEN, wager=10)

	assert b_1.wager == 10
	assert u.balance == 190

	b_2 = u.bet(game=g, player_bet=InOutBets.TEN, wager=-10)

	assert not b_2  # bid should have been deleted
	assert u.balance == 200


def test_negative_bet_cheating(client):
	g = Game.new()
	u = User.new(password_hash="asdkdlj", username="Jean Cheat")
	g.go_to_idle()
	g.go_to_bidable()

	assert u.balance == 200

	b_1 = u.bet(game=g, player_bet=InOutBets.TEN, wager=10)

	assert b_1.wager == 10
	assert u.balance == 190

	b_2 = u.bet(game=g, player_bet=InOutBets.TEN, wager=-15)

	assert not b_2  # bid should have been deleted
	assert u.balance == 200


def test_slot_reservation(client):
	g = Game.new()
	u_1 = User.new(password_hash="asdkdlj", username="Jean Test")
	u_2 = User.new(password_hash="asdkdlj", username="Test Andy")
	g.go_to_idle()
	g.go_to_bidable()

	b_1 = u_1.bet(game=g, player_bet=InOutBets.TEN, wager=10)
	b_2 = u_2.bet(game=g, player_bet=InOutBets.TWENTY, wager=20)

	assert b_1.wager == 10
	assert b_2.wager == 20

	with pytest.raises(Exception):
		u_1.bet(game=g, player_bet=InOutBets.TWENTY, wager=10)

	u_1.bet(game=g, player_bet=InOutBets.TEN, wager=10)

	assert b_1.wager == 20


def test_state_cycle(client):
	g = Game.new()

	for i in range(1, 100):
		g.go_to_idle()
		r = g.get_last_round()
		assert r.round_number == i
		assert r.state == RoundStates.IDLE.value
		g.go_to_bidable()
		r = g.get_last_round()
		assert r.round_number == i
		assert r.state == RoundStates.BIDABLE.value
		g.go_to_waiting()
		r = g.get_last_round()
		assert r.round_number == i
		assert r.state == RoundStates.WAITING.value
		g.go_to_result(Slots.ZERO)
		r = g.get_last_round()
		assert r.round_number == i
		assert r.state == RoundStates.RESULT.value


def test_payout_full(client):
	g = Game.new()
	u_1 = User.new(password_hash="asdkdlj", username="Jean Test")
	u_2 = User.new(password_hash="asdkdlj", username="Test Andy")
	# ---------------------------------------
	g.go_to_idle()

	assert not u_1.bids

	r = g.get_last_round()
	assert r.round_number == 1
	assert r.state == RoundStates.IDLE.value
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

	b_1: Bid = Bid.get_bids_from_round_with_bet(
		round=r, player_bet=InOutBets.ELEVEN
	)
	b_2: Bid = Bid.get_bids_from_round_with_bet(
		round=r, player_bet=InOutBets.TWELVE
	)

	assert b_1.user_id == u_1.id
	assert b_2.user_id == u_2.id

	assert not b_2.is_won
	assert b_2.wager == 30

	assert u_2.bet(game=g, player_bet=InOutBets.TWELVE, wager=-20)
	assert u_2.balance == 190
	assert b_2.wager == 10

	with pytest.raises(Exception):
		u_1.bet(game=g, player_bet=InOutBets.ELEVEN, wager=10000)

	r = g.get_last_round()
	assert r.round_number == 1
	assert r.state == RoundStates.BIDABLE.value
	assert ts == r.timestamp
	assert r.game_id == g.id
	assert not r.winning_slot
	assert not r.get_winning_bids()

	# ------------------------------
	g.go_to_waiting()

	r = g.get_last_round()
	assert r.round_number == 1
	assert r.state == RoundStates.WAITING.value
	assert ts == r.timestamp
	assert r.game_id == g.id
	assert not r.winning_slot
	assert not r.get_winning_bids()

	with pytest.raises(Exception):
		u_1.bet(game=g, player_bet=InOutBets.ELEVEN, wager=10)

	# -----------------------------
	g.go_to_result(Slots.ELEVEN)

	r = g.get_last_round()
	assert r.round_number == 1
	assert r.state == RoundStates.RESULT.value
	assert ts == r.timestamp
	assert r.game_id == g.id
	assert r.winning_slot == Slots.ELEVEN.value
	w_b = r.get_winning_bids()
	assert len(w_b) == 1
	assert w_b[0].is_won


def test_post_bid(client):
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
	
	r2 = client.post(
		"/games/1/bet",
		data=json.dumps(dict(position_id=1, value=5, username="oly")),
		content_type="application/json",
	)
	assert r2.json["balance"] == 190
	assert r2.status_code == 201


	r3 = client.post(
		"/games/1/bet",
		data=json.dumps(dict(position_id=1, value=-5, username="oly")),
		content_type="application/json",
	)
	assert r3.json["balance"] == 195
	assert r3.status_code == 201

	r4 = client.post(
		"/games/1/bet",
		data=json.dumps(dict(position_id=1, value=-10, username="oly")),
		content_type="application/json",
	)
	assert r4.json["balance"] == 200
	assert r4.status_code == 201

def test_login(client):
	User.new(username="oly")
	g = Game.get(1)
	g.go_to_idle()
	g.go_to_bidable()
	r = client.post(
		"/user/login",
		data=json.dumps(dict(username="oly")),
		content_type="application/json",
	)
	assert r.status_code == 200

	assert r.json["username"] == "oly"
	assert isinstance(r.json["balance"], int)
