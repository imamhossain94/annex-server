from bs4 import BeautifulSoup
from flask import request, jsonify
from requests import Session
from requests.utils import dict_from_cookiejar
import requests
import shutil
import tempfile

# Base url
baseUrl = 'https://annex.bubt.edu.bd/'

# Path or Endpoint
loginPath = 'global_file/action/login_action.php'
dashboardPath = 'ONSIS_SEITO/'

# Urls
loginUrl = baseUrl + loginPath
dashboardUrl = baseUrl + dashboardPath

# Header
headers = {
    'Accept': '*/*',
    'Accept-Encoding': "gzip, deflate, br",
    "Connection": "keep-alive",
    'Content-Length': '2134',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'annex.bubt.edu.bd:443'
}


# Login using students id and password
def annexLogin():
    user_name = request.args.get('id')
    pass_word = request.args.get('pass')
    if user_name is not None and pass_word is not None:
        payload = {
            'username': user_name,
            'password': pass_word,
        }
        s = Session()
        res = s.get(baseUrl)
        signin = BeautifulSoup(res.content, 'html.parser')
        payload['admiNlogin'] = signin.find('button', id='logIn_button')['value']
        s.post(loginUrl, data=payload,)
        r = s.get(dashboardUrl)

        print(r.url)

        if r.url == dashboardUrl:
            data = {'status': 'true', 'PHPSESSID': dict_from_cookiejar(s.cookies)['PHPSESSID']}
        else:
            data = {'status': 'false', 'reason': 'ID or Password is invalid!'}
    else:
        data = {'status': 'failed', 'reason': 'ID or Password is not Provided!'}
    response = jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

