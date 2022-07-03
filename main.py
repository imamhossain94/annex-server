import os
import sys
from flask import Flask
from flaskr.route import *

sys.path.insert(0, os.getcwd() + '/apis')

app = Flask(__name__)

app.register_blueprint(annex)


@app.route('/')
def welcome():
    return '<h1 align="center">Server Running Successfully</h1>'