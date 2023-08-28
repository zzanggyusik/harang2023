from flask import Flask
from flask_session import Session

from .instance.config import FLASK_SECRET_KEY, MONGODB_IP, MONGODB_PORT
from . import login, register, remote
from .login import get_login_blueprint
from .register import get_register_blueprint
from .remote import get_remote_blueprint
# from pymongo import MongoClient
# from flask_mongoengine import MongoEngine

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = FLASK_SECRET_KEY
    app.config['SESSION_TYPE'] = 'filesystem'
    # app.config['SESSION_TYPE'] = 'mongodb'
    # app.config['SESSION_MONGODB'] = MongoClient(MONGODB_IP, MONGODB_PORT)['harang']

    # db = MongoEngine(app)
    Session(app)

    app.register_blueprint(get_login_blueprint())
    app.register_blueprint(get_register_blueprint())
    app.register_blueprint(get_remote_blueprint())

    return app



