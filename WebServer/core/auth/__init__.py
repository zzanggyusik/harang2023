from flask import Blueprint
from .routes import initialize_routes

login = Blueprint('login', __name__, url_prefix='/login')
register = Blueprint('register', __name__, url_prefix='/register')
#mypage = Blueprint("maypage", __name__, url_prefix="/mypage")

initialize_routes(login, register) #mypage추가
