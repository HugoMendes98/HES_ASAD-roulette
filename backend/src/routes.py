from flask import request

from . import roulette_logic_blueprint
from .models import User


@roulette_logic_blueprint.post("/user/login")
def login():
	username = request.json.get("username")
	u = User.get(username)
	if u is None:
		u = User.new(username)
	return {"id": u.id, "username": u.username, "balance": int(u.balance)}
