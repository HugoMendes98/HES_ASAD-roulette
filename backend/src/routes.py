from flask import redirect, request, send_file, send_from_directory

from . import roulette_logic_blueprint, roulette_website_blueprint
from .models import User


@roulette_website_blueprint.get("/")
def get_home():
	return redirect("/games/1")

@roulette_website_blueprint.get("/games/<game_id>")
def get_home_gid(game_id):
	return send_file("static/index.html")

@roulette_website_blueprint.get("/games/<game_id>/<path:filename>")
def get_home_(game_id, filename):
	return send_from_directory("static", filename)


@roulette_logic_blueprint.post("/user/login")
def login():
	username = request.json.get("username")
	u = User.get(username)
	if u is None:
		u = User.new(username)
	return {"id": u.id, "username": u.username, "balance": int(u.balance)}
