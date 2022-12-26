from bs4 import BeautifulSoup
from flask import request, jsonify
from requests import Session
from requests.utils import dict_from_cookiejar
from app.v1.constants import *


# Login using students id and password
def annexLogin():
    # get students id from the request arguments
    user_name = request.args.get('id')
    # get students password from the request arguments
    pass_word = request.args.get('pass')

    # checking the student id and password is empty or not
    if user_name is not None and pass_word is not None:
        # creating a payload map/dictionary to send as login data
        payload = {
            'username': user_name,
            'password': pass_word,
        }
        # an object of session
        s = Session()
        # load the annex login page and store the response in a variable named res
        res = s.get(baseUrl)
        # Lets scrap the login page using BeautifulSoup html parser
        login = BeautifulSoup(res.content, 'html.parser')
        # Find an extra hidden field from the login form
        # the extra payload is inside the login button value
        payload['admiNlogin'] = login.find('button', id='logIn_button')['value']

        # lets login using the login url and payload data
        s.post(loginUrl, data=payload, )

        # trying to load the dashboard
        r = s.get(dashboardUrl)

        # if the dashboard load successfully then it is a successful login
        if r.url == dashboardUrl:
            # add the php session id for the future usage
            data = {'status': 'true', 'PHPSESSID': dict_from_cookiejar(s.cookies)['PHPSESSID']}
        else:
            # if the id or password is invalid send this message
            data = {'status': 'false', 'reason': 'ID or Password is invalid!'}
    else:
        # if the students id or password is missing then send this response
        data = {'status': 'false', 'reason': 'ID or Password is not Provided!'}
    # serialize data to JSON and wrap it in a ~app.Response with the application/json mimetype.
    response = jsonify(data)
    # the Access-Control-Allow-Origin response header indicates whether the response can be
    # shared with requesting code from the given origin.
    response.headers.add('Access-Control-Allow-Origin', '*')
    # response the result
    return response
