from flask import redirect, request, jsonify
from.models import User
from . import roulette_website_blueprint

@roulette_website_blueprint.get("/")
def get_home():
    redirect("/game/register")

@roulette_website_blueprint.post("/user/login")
def login():
    username = request.json.get("username")
    u = User.get(username)
    if u is None:
        u = User.new(username)
    return  jsonify({"username": u.username, "balance": int(u.balance)})

def get_user_info():
    pass