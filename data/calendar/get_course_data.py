import json
import requests
import sys

with open('courseDat.json', 'r') as f:
    dat = json.load(f)

items = list(dat.items())
total_num = len(items)

for i, (ID, course) in enumerate(items):
    response = requests.get(f"https://uvic.kuali.co/api/v1/catalog/course/63f510ea5295ea001cb85899/{course['pid']}")
    course = response.json()
    newInfo = {
        'description': course.get('description'),
        'notes': course.get('supplementalNotes'),
        'credits': course.get('credits'),
        'crossListed': course.get('crossListedCourses'),
        'hours': course.get('hoursCatalogText')
    }

    dat[ID].update(newInfo)
    sys.stdout.write('\r')
    sys.stdout.write(f'{i/total_num * 100:.2f}% complete. Doing {ID} now. \nGot {course.get("description")}')
    sys.stdout.flush()

obj = json.dumps(dat, indent=2)

with open('course_data.json', 'w') as f:
    f.write(obj)