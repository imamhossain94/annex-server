import os
import sys

from bs4 import BeautifulSoup


def generateClassObj(day, time, cls, link):
    classObj = {
        'day': day,
        'schedule': {
            'start': time.split('to')[0].strip(),
            'end': time.split('to')[0].strip(),
            'timeObj': time
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


final_data = {
    'data': list()
}

try:
    f = open(f"{os.path.dirname(sys.argv[0])}/routine.html", "r", encoding='utf-8')
    routineHtml = f.read()

    rows = BeautifulSoup(str(routineHtml), 'html.parser').findAll('tr')
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
                    time = timeList[td.index(d)+1]
                    cls = d.text.strip().split('\n')
                    link = d.find('a').attrs['href']

                    final_data['data'].append(generateClassObj(day=day, time=time, cls=cls, link=link))
                    final_data['status'] = 'success'
                    final_data['type'] = 'Class Routine'

except Exception as e:
    final_data = {'status': 'failed', 'reason': str(e)}

# response = jsonify(final_data)
# response.headers.add('Access-Control-Allow-Origin', '*')

print(final_data)
