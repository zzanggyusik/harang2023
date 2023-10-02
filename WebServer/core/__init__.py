from flask import Flask

from .instance.config import FlaskConfig, MongoDBConfig
from .auth import login as login_blueprint
from .auth import register as register_blueprint
from .remote import remote as remote_blueprint
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

    app.register_blueprint(login_blueprint)
    #app.register_blueprint(mypage_blueprint)
    app.register_blueprint(register_blueprint)
    app.register_blueprint(remote_blueprint)
    #app.register_blueprint(history)
    #app.register_blueprint(market)

    return app
