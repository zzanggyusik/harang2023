from flask import Blueprint
from .routes import initialize_routes

remote = Blueprint("remote", __name__, url_prefix="/remote")
initialize_routes(remote)

