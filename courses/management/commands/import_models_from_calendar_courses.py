
from django.core.management.base import BaseCommand
from django.template.defaultfilters import slugify
from courses.models import Course, Program
import json
import re
class Command(BaseCommand):
    help = 'Add course links'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str, help='The JSON file to load calendar data from')

    def handle(self, *args, **options):
        '''Usage: python manage.py add_course_links.py <filename>'''
           

        filename = options['filename']
        with open(filename, 'r') as f:
            data = json.load(f)

            for item in data:
                key = str(item)

                # Modify Course instances to include links to uvic calendar, descriptions, and notes.      
                slug = slugify(data[key]['courseID'])
                print(slug, data[key]['description'], data[key]['notes'], "https://www.uvic.ca/calendar/future/undergrad/index.php#/courses/"+data[key]['pid'], sep='\n', end='\n'+25*'-')
                # print(slug)
                program_subject = re.findall(r'[A-Z]{2,4}', data[key]['courseID'])[0]
                course_number = re.findall(r'\d{3,4}[a-zA-Z]?\d?', data[key]['courseID'])[0]
                try:
                    program_instance = Program.objects.get(subject=program_subject)
                except Program.DoesNotExist:
                    print("NEW PROGRAM\n\n\n\n\n")
                    program_instance = Program(subject=program_subject, subjectDescription=data[key]['subjectDescription'])
                    program_instance.save()

                try:
                    course_instance = Course.objects.get(slug=slug)
                    course_instance.description = data[key]['description']
                    course_instance.notes = data[key]['notes']
                    course_instance.link = "https://www.uvic.ca/calendar/future/undergrad/index.php#/courses/"+data[key]['pid']
                    course_instance.save()
                except Course.DoesNotExist:
                    course_instance = Course(
                        program=program_instance,
                        courseNumber=course_number,
                        courseTitle=data[key]['title'],
                        )
                    course_instance.save()
                    
             
             ### TODO: Add many-to-many relation between Course and Degree.
                # Need to go through data[key]['requirements'] and parse it into a list of courses.
                # Additionally there will be logic tied to the courses and will have to create a 
                # new model: CourseRequirement that will have a many-to-many relations with Course and Degree.
                # can use similar regex from import_models_from_calendar_degrees.py to get the courses.