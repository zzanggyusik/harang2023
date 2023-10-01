from flask import Blueprint
from .routes import initialize_routes

history = Blueprint("history", __name__, url_prefix="/history")
initialize_routes(history)