# This could be improved and made much faster by creating a JSON file for all the courses 
# that contains the descriptions and links. It would be a matter of combining two JSON files 
# (the one used in this script and the one used in import_models_from_banner.py)
# and then when bulk creating the courses, all the data is already there.

# This would DRASTICALLY improve the speed of this script. Like from 10 minutes to 10 seconds.
# However, I don't mind leaving this one as is as a reminder...

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

                # Get program code
                program_subject = re.findall(r'[A-Z]{2,4}', data[key]['courseID'])[0]
                course_number = re.findall(r'\d{3,4}[a-zA-Z]?\d?', data[key]['courseID'])[0]
                try:
                    program_instance = Program.objects.get(subject=program_subject)
                except Program.DoesNotExist:
                    print("NEW PROGRAM\n\n\n\n\n")
                    program_instance = Program(subject=program_subject, subjectDescription=data[key]['subjectDescription'])
                    program_instance.save()

                for term in ["202309", "202401"]:     
                    slug = slugify(data[key]['courseID']+'-'+term)
                    print(slug, data[key]['description'], data[key]['notes'], "https://www.uvic.ca/calendar/future/undergrad/index.php#/courses/"+data[key]['pid'], sep='\n', end='\n'+25*'-')

                    try:
                        course_instance = Course.objects.get(slug=slug)
                        course_instance.description = data[key]['description']
                        course_instance.notes = data[key]['notes']
                        # Maybe change this to just use a local file and download the required data beforehand.
                        course_instance.link = "https://www.uvic.ca/calendar/future/undergrad/index.php#/courses/"+data[key]['pid']
                        course_instance.save()
                    except Course.DoesNotExist:

                        # This would create a course instance for courses that aren't in the fall or spring.
                        # but I don't need it. If that changes then we can write a new script to bring them in.

                        # course_instance = Course.objects.get_or_create(
                        #     program=program_instance,
                        #     courseNumber=course_number,
                        #     courseTitle=data[key]['title'],
                        #     term="NA",
                        #     )[0]
                        # course_instance.save()

                        print("Course that is not in fall or spring as of Aug 20th.\n\n")
                    
             
             ### TODO: Add many-to-many relation between Course and Degree.
                # Need to go through data[key]['requirements'] and parse it into a list of courses.
                # Additionally there will be logic tied to the courses and will have to create a 
                # new model: CourseRequirement that will have a many-to-many relations with Course and Degree.
                # can use similar regex from import_models_from_calendar_degrees.py to get the courses.