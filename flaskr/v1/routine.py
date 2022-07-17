import asyncio

import nest_asyncio
from bs4 import BeautifulSoup
from flask import request, jsonify
from requests import get

from flaskr.v1.helper.take_screenshot import *
from flaskr.v1.service.services import *


# Get students routine
async def studentRoutine():
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

                try:
                    loop = asyncio.get_running_loop()
                except RuntimeError:  # no event loop running:
                    loop = asyncio.new_event_loop()
                    loop.run_until_complete(take_screenshot(
                        file_name=fileName,
                        url=routineUrl,
                        phpsessid=phpsessid
                    ))
                else:
                    nest_asyncio.apply(loop)
                    asyncio.run(take_screenshot(
                        file_name=fileName,
                        url=routineUrl,
                        phpsessid=phpsessid
                    ))

                routine_image_url = uploadImage(fileName)

                data = {
                    'url': routine_image_url,
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
