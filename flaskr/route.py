from flask import Blueprint
from flaskr.v1.login import *
from flaskr.v1.profile import *

annex = Blueprint('annex', __name__)


@annex.route('/annex/v1/login', methods=['GET'])
def login():
    return annexLogin()


@annex.route('/annex/v1/profile', methods=['GET'])
def profile():
    return studentProfile()
