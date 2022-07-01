from flask import Blueprint
from flaskr.v1.login import *

annex = Blueprint('annex', __name__)


@annex.route('/annex/v1/login', methods=['GET'])
def login():
    return annexLogin()
