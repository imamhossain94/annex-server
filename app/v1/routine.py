import nest_asyncio
from bs4 import BeautifulSoup
from flask import request, jsonify
from requests import get

from app.v1.helper.take_screenshot import *
from app.v1.service.services import *


def generateClassObj(day, period, cls, link):
    classObj = {
        'day': day,
        'schedule': {
            'start': period.split('to')[0].strip(),
            'end': period.split('to')[0].strip(),
            'timeObj': period
        },
        'programCode': cls[0].split(' ')[0],
        'courseCode': cls[0].split(' ')[1],
        'facultyCode': cls[1].split(':')[1].strip(),
        'facultyLink': link.replace(' ', '%20'),
        'building': cls[2].split('⇒')[0].replace('B:', '').strip(),
        'room': cls[2].split('⇒')[1].replace('R:', '').strip(),
        'intake': cls[3].split('-')[0].replace('Intake:', '').strip(),
        'section': cls[3].split('-')[1].replace('Intake:', '').strip()
    }

    return classObj


# Get students routine
async def studentRoutine():
    # get requested users session id from the request arguments
    phpsessid = request.args.get('phpsessid')
    routine_type = request.args.get('type') or 'data'
    data = {}
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
                # create a data dictionary to respond
                data = {'data': list()}
                routine_table = routine.find_all('table')[1]

                # Save routine table html
                # with open('routine.html', 'w', encoding='utf-8') as f:
                #     f.write(str(routine_table))

                rows = routine_table.findAll('tr')
                timeList = []

                for i in range(len(rows)):
                    row = rows[i]
                    th = row.find_all('th')
                    td = row.find_all('td')
                    if i == 0:
                        for j in th:
                            timeList.append(j.text)
                    else:
                        for d in td:
                            if d.text.strip():
                                day = th[0].text
                                period = timeList[td.index(d)+1]
                                cls = d.text.strip().split('\n')
                                link = d.find('a').attrs['href']

                                data['data'].append(generateClassObj(day=day, period=period, cls=cls, link=link))
                data['status'] = 'success'
                data['type'] = 'data'

            elif routine_type == 'image':
                fileName = std_name + '_' + std_id
                routine_image_url = await take_screenshot(file_name=fileName, url=routineUrl, phpsessid=phpsessid)
                data = {
                    'url': routine_image_url,
                    'status': 'true',
                    'type': 'image'
                }
        else:
            # if the url failed to load then send this response
            data = {'status': 'false', 'reason': 'phpsessid expired!'}
    else:
        # if the phpsessid is missing then send this response
        data = {'status': 'false', 'reason': 'phpsessid is not Provided!'}
    # serialize data to JSON and wrap it in a ~app.Response with the application/json mimetype.
    response = jsonify(data)
    # the Access-Control-Allow-Origin response header indicates whether the response can be
    # shared with requesting code from the given origin.
    response.headers.add('Access-Control-Allow-Origin', '*')
    # response the result
    return response
