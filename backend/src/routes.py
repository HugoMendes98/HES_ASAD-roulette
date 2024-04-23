from flask import jsonify, redirect, request

from . import roulette_website_blueprint
from .models import User


def register_routes():
	# Only want to register the routes below
	pass


@roulette_website_blueprint.get("/")
def get_home():
	redirect("/game/register")


@roulette_website_blueprint.post("/user/login")
def login():
	username = request.json.get("username")

	u = User.get(username)
	if u is None:
		u = User.new(username)
	return jsonify({"username": u.username, "balance": u.balance})
