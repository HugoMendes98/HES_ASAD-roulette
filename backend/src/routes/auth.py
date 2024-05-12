from flask import Blueprint, request

from ..models import User
from .common import API_PREFIX

auth_blueprint = Blueprint("auth", __name__, url_prefix=API_PREFIX + "/auth")


@auth_blueprint.post("/login")
def login():
	username = request.json.get("username")
	u = User.get(username)

	# FIXME: to remove and use signup (and some user info? only with /me)
	if u is None:
		u = User.new(username)
	return {"id": u.id, "username": u.username, "balance": int(u.balance)}


@auth_blueprint.post("/signup")
def signup():
	# TODO: Create a user and return auth_token (and some user info? only with /me)
	return "Not implemented", 501


@auth_blueprint.post("/refresh")
def refresh():
	# TODO: test given auth token and return a new one
	return "Not implemented", 501


@auth_blueprint.post("/me")
def get_connected():
	# TODO: validate given auth token and return associated user
	return "Not implemented", 501
