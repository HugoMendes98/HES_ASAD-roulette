import flask
from flask_jwt_extended import (
	create_access_token,
	decode_token,
	get_jwt_identity,
	get_jwt_request_location,
)
from werkzeug.exceptions import Unauthorized

from ..models import User

# Use theses instead of JWT middlewares to use the type returns


def get_encoded_token_from_request(request: flask.Request):
	location = get_jwt_request_location()

	if location == "headers":
		# remove the `Bearer `
		return request.headers["Authorization"][7:]

	# TODO: the others ?

	return None


def get_user_from_jwt(jwt_identity):
	"""
	Get the user from the jwt_identity
	"""
	return User.get_by_id(jwt_identity["userId"])


def get_current_user():
	"""
	Get the user from the jwt of the library
	"""
	user = get_user_from_jwt(get_jwt_identity())
	if user is None:
		raise Unauthorized("Auth invalid (or no longer)")

	return user


def get_token_dict(token: str):
	"""
	Generates the jwt token and returns a dict with information
	"""
	decoded = decode_token(token)
	user = get_user_from_jwt(decoded["sub"])
	if user is None:
		raise Unauthorized("Auth invalid (or no longer)")

	exp = decoded["exp"] * 1000
	iat = decoded["iat"] * 1000

	return {
		"info": {"duration": exp - iat, "emitted_at": iat, "expire_at": exp},
		"user": user.to_json(),
		"token": token,
	}


def generate_token_dict(user: User):
	"""
	Generates the jwt token and returns a dict with information
	"""
	return get_token_dict(create_access_token({"userId": user.id}))
