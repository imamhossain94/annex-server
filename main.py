import sys

# Load .env file
from dotenv import load_dotenv
from flask import Flask

load_dotenv()

from app.route import *

sys.path.insert(0, os.getcwd() + '/apis')

app = Flask(__name__)

app.register_blueprint(annex)


@app.route('/')
def welcome():
    return '<h1 align="center">Server Running Successfully</h1>'
