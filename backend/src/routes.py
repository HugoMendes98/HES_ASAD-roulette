from flask import redirect, request, send_file

from . import roulette_logic_blueprint, roulette_website_blueprint
from .models import User


@roulette_website_blueprint.get("/")
def get_home():
	return redirect("/games/1")

@roulette_website_blueprint.get("/games/<game_id>")
def get_home_gid(game_id):
	return send_file("static/index.html")


@roulette_logic_blueprint.post("/user/login")
def login():
	username = request.json.get("username")
	u = User.get(username)
	if u is None:
		u = User.new(username)
	return {"id": u.id, "username": u.username, "balance": int(u.balance)}
