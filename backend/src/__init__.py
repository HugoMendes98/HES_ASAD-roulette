from flask import Blueprint

roulette_logic_blueprint = Blueprint(
	"roulette_logic", __name__, url_prefix="/api/games/"
)
