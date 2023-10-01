from flask import Flask

from .instance.config import FlaskConfig, MongoDBConfig
from . import login, register, remote #mypage, history, market
from datetime import timedelta

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

    app.register_blueprint(login)
    app.register_blueprint(register)
    #app.register_blueprint(mypage)
    app.register_blueprint(remote)
    #app.register_blueprint(history)
    #app.register_blueprint(market)

    return app
