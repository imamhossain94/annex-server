import asyncio

from flask import Blueprint

from app.v1.login import *
from app.v1.profile import *
from app.v1.routine import *

annex = Blueprint('annex', __name__)


@annex.route('/annex/v1/login', methods=['GET'])
def login():
    return annexLogin()


@annex.route('/annex/v1/profile', methods=['GET'])
def profile():
    return studentProfile()


@annex.route('/annex/v1/routine', methods=['GET'])
def routine():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:  # no event loop running:
        loop = asyncio.new_event_loop()
        return loop.run_until_complete(studentRoutine())
    else:
        nest_asyncio.apply(loop)
        return asyncio.run(studentRoutine())

