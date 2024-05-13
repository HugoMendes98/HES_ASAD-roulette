from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from ..models import User
from . import auth_utils
from .common import API_PREFIX

auth_blueprint = Blueprint("auth", __name__, url_prefix=API_PREFIX + "/auth")


@auth_blueprint.post("/login")
def login():
	username = request.json.get("username")
	password = request.json.get("password")

	user = User.get_by_credentials(username, password)
	if user is None:
		return "Forbidden", 401

	return auth_utils.generate_token_dict(user)


@auth_blueprint.post("/signup")
def signup():
	username = request.json.get("username")
	password = request.json.get("password")

	if User.get_by_username(username) is not None:
		return "Already exists", 409

	return auth_utils.generate_token_dict(User.new(username, password))


@auth_blueprint.post("/refresh")
@jwt_required()
def refresh():
	return auth_utils.generate_token_dict(auth_utils.get_current_user())


@auth_blueprint.get("/me")
@jwt_required()
def get_connected():
	return auth_utils.get_token_dict(
		auth_utils.get_encoded_token_from_request(request)
	)
