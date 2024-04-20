from flask import Blueprint

roulette_logic_blueprint = Blueprint("roulette_logic", __name__, url_prefix="/game/")

roulette_website_blueprint = Blueprint(
    "website", __name__, url_prefix="", template_folder="templates", static_folder="static"
)