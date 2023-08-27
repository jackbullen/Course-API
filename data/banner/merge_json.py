# dont judge me for this one... it gets the job done.

import json
import os

dat = dict()
fall = []
spring = []

# ls data/fall/
#offset0.json     offset1500.json  offset2500.json  offset3500.json
#offset1000.json  offset2000.json  offset3000.json  offset500.json
#ls data/spring/
#offset0.json     offset1500.json  offset2500.json  offset3500.json
#offset1000.json  offset2000.json  offset3000.json  offset500.json
# lol

# collect spring dataset
for _,_, files in os.walk("./spring/"):
    for file in files:
        with open("./spring/"+file) as f:
            json_data = f.read()
        spring.append(json.loads(json_data))

# collect fall dataset
for _, _, files in os.walk("./fall/"):
    for file in files:
        with open("./fall/"+file) as f:
            json_data = f.read()
        fall.append(json.loads(json_data))

# load fall and spring datasets into dat.
for courses in fall:
    for course in courses['data']:
        dat[course['id']] = course
for courses in spring:
    for course in courses['data']:
        dat[course['id']] = course

# write dat to courses.json
with open("courses.json", "w") as json_file:
    json.dump(dat, json_file)