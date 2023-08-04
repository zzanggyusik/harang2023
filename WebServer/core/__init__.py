from flask import Flask
from . import login
from .instance.config import *

# app Init
app = Flask(__name__)
app.config['SECRET_KEY'] = FLASK_SECRET_KEY

# Set BluePrint
app.register_blueprint(login.login)
