from flask import Blueprint
from .routes import initialize_routes

market = Blueprint("market", __name__, url_prefix="/market")
initialize_routes(market)