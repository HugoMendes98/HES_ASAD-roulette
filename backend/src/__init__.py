from flask import Blueprint

roulette_logic_blueprint = Blueprint(
	"roulette_logic", __name__, url_prefix="/api/games/"
)

roulette_website_blueprint = Blueprint(
	"website",
	__name__,
	url_prefix="",
	template_folder="templates",
	static_folder="static",
	static_url_path="",
)
