from flask import Flask

from .instance.config import FlaskConfig, MongoDBConfig
from . import login, register, remote, history
from .login import get_login_blueprint
from .register import get_register_blueprint
from .remote import get_remote_blueprint
from .history import get_history_blueprint
from datetime import timedelta
# from pymongo import MongoClient
# from flask_mongoengine import MongoEngine

def create_app():
    app = Flask(__name__)
    flask = FlaskConfig()
    
    app.config['SECRET_KEY'] = flask.secret_key
    app.config['SESSION_TYPE'] = flask.session_type
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes= 60)
    
    # app.config['SESSION_TYPE'] = 'mongodb'
    # app.config['SESSION_MONGODB'] = MongoClient(MONGODB_IP, MONGODB_PORT)['harang']

    # db = MongoEngine(app)
    # Session(app)

    app.register_blueprint(get_login_blueprint())
    app.register_blueprint(get_register_blueprint())
    app.register_blueprint(get_remote_blueprint())
    app.register_blueprint(get_history_blueprint())

    return app



