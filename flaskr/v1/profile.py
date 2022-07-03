from bs4 import BeautifulSoup
from flask import request, jsonify
from requests import get
from flaskr.service.services import *
from flaskr.v1.constants import *


# Get students basic information
def studentProfile():

    # get requested users session id from the request arguments
    phpsessid = request.args.get('phpsessid')

    # checking the student id and phpsessid is empty or not
    if phpsessid is not None:

        # creating a cookies payload
        cookies = {'PHPSESSID': phpsessid}

        # request for the students dashboard with his/her cookies
        res = get(dashboardUrl, cookies=cookies)

        # if the url load successfully start scrapping
        if res.url == dashboardUrl:

            # Lets scrap the students dashboard using BeautifulSoup html parser
            dashboard = BeautifulSoup(str(res.text), 'html.parser')

            # First find a div with "user-info" class
            userInfo = dashboard.find('div', attrs={'class': 'user-info'})

            # Then find all the strong with "ribbon-content" class
            infoList = userInfo.findAll('strong', attrs={'class': 'ribbon-content'})

            # infoList will be an array
            # the 0th index of it will be the students name
            std_name = infoList[0].get_text()

            # the 1st index of it will be the students id
            std_id = infoList[1].get_text()

            # the 2nd index of it contains the students intake and section
            # first replace extra spaces from the string
            # then split it with this '-' character. it will generate an list
            # 0th index is the students intake
            # 1st index is the students section
            std_intake_section = infoList[2].get_text().replace(' ', '')
            std_intake = std_intake_section.split('-')[0]
            std_section = std_intake_section.split('-')[1]

            # the 3rd index of it contains the students intake and section
            # first split it with this '(' character. it will generate an list
            # 0th index is the students program
            # 1st index is the students semester_type. we have to replace an extra character ')'
            std_program_semester = infoList[3].get_text()
            std_program = std_program_semester.split('(')[0].strip()
            std_semester_type = std_program_semester.split('(')[1].strip().replace(')', '')

            # Lets get the students profile picture
            proPic = dashboard.find('div', attrs={'id': 'proPic'})

            # call uploadImage method get the students image url
            # it will take two parameters
            # first one is file_name
            # second one is image src
            std_image_url = uploadImage(std_name + '_' + std_id, proPic.find('img')['src'])

            # create a data dictionary to respond
            data = {
                'id': std_id,
                'name': std_name,
                'intake': std_intake,
                'section': std_section,
                'program': std_program,
                'semester_type': std_semester_type,
                'image_url': std_image_url,
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
