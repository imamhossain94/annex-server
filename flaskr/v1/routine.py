from bs4 import BeautifulSoup
from flask import request, jsonify
from requests import get
from flaskr.v1.constants import *
from flaskr.v1.service.services import *
from flaskr.v1.helper.web_image import *


# Get students routine
def studentRoutine():

    # get requested users session id from the request arguments
    phpsessid = request.args.get('phpsessid')
    routine_type = request.args.get('type') or 'data'

    # checking the student id and phpsessid is empty or not
    if phpsessid is not None:

        # creating a cookies payload
        cookies = {'PHPSESSID': phpsessid}

        # request for the students dashboard with his/her cookies
        res = get(routineUrl, cookies=cookies)

        # if the url load successfully start scrapping
        if res.url == routineUrl:

            # Lets scrap the students routine using BeautifulSoup html parser
            routine = BeautifulSoup(str(res.text), 'html.parser')

            userInfo = routine.find('div', attrs={'class': 'user-info'})
            infoList = userInfo.findAll('strong', attrs={'class': 'ribbon-content'})
            std_name = infoList[0].get_text()
            std_id = infoList[1].get_text()

            if routine_type == 'data':
                print(routine)
                # create a data dictionary to respond
                data = {
                    'id': "lala",
                    'status': 'true',
                }

            elif routine_type == 'image':
                fileName = std_name + '_' + std_id
                # open_url(
                #     file_name=fileName,
                #     address=routineUrl,#'https://annex.bubt.edu.bd/ONSIS_SEITO/includes/helpers/routine_format.php',
                #     phpsessid=phpsessid
                # )

                b = 'https://render-tron.appspot.com/screenshot/'
                r = get(routineUrl, stream=True, cookies=cookies)
                with open('xyz.png', 'wb') as file:
                    for x in r:
                        file.write(x)

                # routine_image_url = uploadImage(fileName)

                data = {
                    'url': 'routine_image_url',
                    'status': 'true',
                }
        else:
            # if the url failed to load then send this response
            data = {'status': 'false', 'reason': 'phpsessid expired!'}
    else:
        # if the phpsessid is missing then send this response
        data = {'status': 'false', 'reason': 'phpsessid is not Provided!'}
    # serialize data to JSON and wrap it in a ~flask.Response with the application/json mimetype.
    response = jsonify(data)
    # the Access-Control-Allow-Origin response header indicates whether the response can be
    # shared with requesting code from the given origin.
    response.headers.add('Access-Control-Allow-Origin', '*')
    # response the result
    return response
