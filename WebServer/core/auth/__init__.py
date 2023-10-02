from flask import Blueprint
from .routes import initialize_routes

login = Blueprint('login', __name__, url_prefix='/login')
logout = Blueprint('logout', __name__, url_prefix='/loout')
register = Blueprint('register', __name__, url_prefix='/register')
#mypage = Blueprint("maypage", __name__, url_prefix="/mypage")

initialize_routes(login, logout, register) #mypage추가
