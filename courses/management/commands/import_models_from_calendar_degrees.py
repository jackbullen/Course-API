import json
from django.core.management.base import BaseCommand
from django.template.defaultfilters import slugify
from courses.models import Faculty, MeetingTime, Course, Program, MeetingLocation, Section, InstructorRole, CourseLabLink, CourseTutorialLink, Degree, Specialization
import re 
from collections import Counter

# TODO: In models.py merge CourseLabLink and CourseTutorialLink into CourseSectionLink by adding parameter and import instances from data here.

# stackoverflow.com/questions/1835756 
# if you expect that 99 % of the time result will actually contain something iterable, I'd use the try/except approach. It will be faster if exceptions really are exceptional. If result is None more than 50 % of the time, then using if is probably better.
# tldr: if exception rare, use try/except. if exception common, use if/else.
# reasoning if if shuts down right away whereas trys will keep going until it hits an exception, so it may run more often.

class Command(BaseCommand):
    help = 'Load data from JSON file into models'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str, help='The JSON file to load calendar data from')

    def handle(self, *args, **options):
        '''Usage: python manage.py import_models_from_calendar <filename>'''
           
         
        filename = options['filename']
        with open(filename, 'r') as f:
            data = json.load(f)
           
            for item in data:
                key =  str(item)

                # Get program code
                try:
                    courses = re.findall(r'([A-Z]{2,4}\d{3}[A-Z]?\d?|[A-Z]{2,4})', data[key]['requirements'])
                    potential_program_codes = [re.findall(r'[A-Z]{2,4}', code)[0] for code in courses]
                    program_code = Counter(potential_program_codes).most_common(1)[0][0]
                except:
                    # there are six of these cases, which we can put in as law and change after.
                    #  there are four that are not law: MNR-CSSY: ECE, MNR-ELSY: ECE, MNR-MESY: MECH, BA-RHAH: EPHE
                    program_code = "LAW"
                                   
                # Get program instance
                try:
                    program_instance = Program.objects.get(subject=program_code)
                except Program.DoesNotExist:
                    program_instance = None
                    continue
                
                # Create Degree Instance
                degree_data = {
                    'code': data[key]['code'],
                    'cred': data[key]['cred'],
                    'program': program_instance,
                    'description': data[key].get('description'),
                    'link': "https://www.uvic.ca/calendar/future/undergrad/index.php#/programs/"+data[key].get('pid'),
                    'requirements': data[key].get('requirements'),
                    'notes': data[key].get('notes'),
                }
                degree_instance = Degree.objects.get_or_create(**degree_data)[0]

                # Create Specialization Instances
                for spec in data[key]['specializations']:
                    Specialization.objects.get_or_create(
                        degree = degree_instance,
                        requirements = spec.get('requirements'),
                        title = spec.get('title'),
                        notes = spec.get('concentrationProgramNotes'),
                    )
            