from flask import redirect
from . import roulette_website_blueprint

@roulette_website_blueprint.get("/")
def get_home():
    redirect("/game/register")