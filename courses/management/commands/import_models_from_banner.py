import json
from django.core.management.base import BaseCommand
from django.template.defaultfilters import slugify
from courses.models import Faculty, MeetingTime, Course, Program, MeetingLocation, Section, InstructorRole, CourseSectionLink

faculty_fields = ['bannerId', 'displayName', 'emailAddress']
meeting_time_fields = ['term', 'beginTime', 'endTime', 'startDate', 'endDate', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
meeting_location_fields = ['building', 'buildingDescription', 'campus', 'campusDescription', 'room']
course_fields = ['term', 'courseNumber', 'courseTitle', 'creditHours']
section_fields = ['id', 'term', 'courseReferenceNumber', 'sequenceNumber', 'scheduleTypeDescription', 'instructionalMethod', 'maximumEnrollment', 'enrollment', 'seatsAvailable', 'waitCapacity', 'waitCount', 'waitAvailable']

class Command(BaseCommand):
    help = 'Load data from JSON file into models'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str, help='The JSON file to load courses from')

    def handle(self, *args, **options):
        '''Usage: python manage.py import_models <filename>'''
           

        filename = options['filename']
        with open(filename, 'r') as f:
            data = json.load(f)
            data = data.items()
            length = len(data)

            PROGRAMS = dict()
            FACULTIES = []
            MEETING_TIMES = []
            MEETING_LOCATIONS = []
            COURSES = dict()
            SECTIONS = []
            INSTRUCTOR_ROLES = []

            for i, (key, section) in enumerate(data):
                key = str(key)
                
                # Create Program instances            
                program_data = {
                    'subject': section['subject'],
                    'subjectDescription': section['subjectDescription']
                }
                program_instance = Program(**program_data)
                PROGRAMS[section['subject']] = program_instance


                # Create MeetingTime instances
                meetingTime_instances = []
                meeting_time_data = section['meetingsFaculty']
                for meeting_time in meeting_time_data:
                    valid_meeting_time = {field: meeting_time['meetingTime'][field] for field in meeting_time_fields}
                    meeting_time_instance = MeetingTime(**valid_meeting_time)
                    meetingTime_instances.append(meeting_time_instance)
                    MEETING_TIMES.append(meeting_time_instance)


                # Create MeetingLocation instances
                meetingLocation_instances = []
                meeting_location_data = section['meetingsFaculty']
                for meeting_location in meeting_location_data:
                    valid_meeting_location = {field: meeting_location['meetingTime'][field] for field in meeting_location_fields}
                    meeting_location_instance = MeetingLocation(**valid_meeting_location)
                    meetingLocation_instances.append(meeting_location_instance)
                    MEETING_LOCATIONS.append(meeting_location_instance)

            Program.objects.bulk_create(list(PROGRAMS.values()))
            print("Programs and meetings loaded into db.")

            for i, (key, section) in enumerate(data):
                program_instance = PROGRAMS[section['subject']]

                # Create Course instances
                valid_course_data = {field: section[field] for field in course_fields}
                slug = slugify(program_instance.subject + valid_course_data['courseNumber'] + '-' + valid_course_data['term'])
                valid_course_data.update({'program': program_instance, 'slug': slug})

                course_instance = Course(**valid_course_data)
                COURSES[slug] = course_instance
            Course.objects.bulk_create(list(COURSES.values()))
            print("Courses loaded into db.")

            for i, (key, section) in enumerate(data):
                program_instance = PROGRAMS[section['subject']]
                course_instance = COURSES[slugify(program_instance.subject + section['courseNumber'] + '-' + section['term'])]

                # Create Section instances
                valid_section_data = {field: section[field] for field in section_fields}
                valid_section_data.update({'course': course_instance})
                section_instance = Section(**valid_section_data)
                # section_instance.meetingLocation.add(*meetingLocation_instances)
                # section_instance.meetingTime.add(*meetingTime_instances)
                SECTIONS.append(section_instance)

                # Create Faculty instances
                valid_faculty_data = []
                for j, faculty in enumerate(section['faculty']):
                    valid_faculty = {field: faculty[field] for field in faculty_fields}
                    valid_faculty.update({'program': program_instance})
                    faculty_instance = Faculty(**valid_faculty) 
                    FACULTIES.append(faculty_instance)
                    
                    # Create InstructorRole instances
                    valid_instructor_role_data = {
                        'faculty': faculty_instance,
                        'section': section_instance,
                        'primaryInstructor': faculty['primaryIndicator']
                    }
                    instructor_role_instance = InstructorRole(**valid_instructor_role_data)
                    INSTRUCTOR_ROLES.append(instructor_role_instance)

            print("Loading rest of objects into db...")
            
            MeetingTime.objects.bulk_create(MEETING_TIMES)
            MeetingLocation.objects.bulk_create(MEETING_LOCATIONS)
            Faculty.objects.bulk_create(FACULTIES)
            Section.objects.bulk_create(SECTIONS)
            InstructorRole.objects.bulk_create(INSTRUCTOR_ROLES)

            self.stdout.write(self.style.SUCCESS('\nLoaded all data into db.\n'))
