import json
import requests
import sys

with open('degrees.json', 'r') as f:
    degrees = json.load(f)

total_num = len(degrees)

degreesDat = {}
for i, deg in enumerate(degrees):
    response = requests.get(f"https://uvic.kuali.co/api/v1/catalog/program/63f510ea5295ea001cb85899/{deg['pid']}")
    dat = response.json()
    print(dat)
    degreesDat[deg['code']] = {
        'cred': deg['credentialType']['name'],
        'code': deg['code'],
        'subject': deg['title'],
        'description': dat.get('description'),
        'requirements': dat.get('programRequirements'),
        'requirementsRtf': dat.get('programRequirementsRtf'),
        'admission': dat.get('admissionRequirementsRtf'),
        'specializations': dat.get('specializations'),
        'notes': dat.get('programNotes'),
        'coop': dat.get('co0pRequirements'),
        'pid': dat.get('pid'),
    }
    sys.stdout.write('\r')
    sys.stdout.write(f'{i/total_num * 100:.2f}% complete. [{"#"*int((i/total_num * 30)):29s}]')
    sys.stdout.flush()

obj = json.dumps(degreesDat, indent=2)

with open('degrees_data.json', 'w') as f:
    f.write(obj)