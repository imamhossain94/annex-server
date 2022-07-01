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
        data = {
            'username': user_name,
            'password': pass_word,
        }
        s = Session()
        # s.get(baseUrl)
        ch = ensure_content_length(baseUrl, session=s)
        s.post(
            loginUrl,
            data=data,
            headers={
                'Accept': '*/*',
                'Accept-Encoding': "gzip, deflate, br",
                "Connection": "keep-alive",
                'Content-Length': ch.headers['Content-Length'],
                'Content-Type': 'application/x-www-form-urlencoded',
                'Host': 'annex.bubt.edu.bd:443'
            }
        )
        r = s.get(baseUrl)
        print(r.url)

        if r.url == baseUrl:
            data = {'status': 'true', 'PHPSESSID': dict_from_cookiejar(s.cookies)['PHPSESSID']}
        else:
            data = {'status': 'false', 'reason': 'ID or Password is invalid!'}
    else:
        data = {'status': 'failed', 'reason': 'ID or Password is not Provided!'}
    response = jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


def ensure_content_length(
    url, *args, method='GET', session=None, max_size=2**20,  # 1Mb
    **kwargs
):
    kwargs['stream'] = True
    session = session or requests.Session()
    r = session.request(method, url, *args, **kwargs)
    if 'Content-Length' not in r.headers:
        # stream content into a temporary file so we can get the real size
        spool = tempfile.SpooledTemporaryFile(max_size)
        shutil.copyfileobj(r.raw, spool)
        r.headers['Content-Length'] = str(spool.tell())
        spool.seek(0)
        # replace the original socket with our temporary file
        r.raw._fp.close()
        r.raw._fp = spool
    return r

