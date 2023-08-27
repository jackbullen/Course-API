import json
from django.core.management.base import BaseCommand
from django.template.defaultfilters import slugify
from courses.models import Faculty, MeetingTime, Course, Program, MeetingLocation, Section, InstructorRole, CourseLabLink, CourseTutorialLink

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

            for item in data:
                key = str(item)
                
                # Create Program instances            
                program_data = {
                    'subject': data[key]['subject'],
                    'subjectDescription': data[key]['subjectDescription']
                }
                program_instance = Program.objects.get_or_create(**program_data)[0]

                # Create Faculty instances
                valid_faculty_data = []
                for faculty in data[key]['faculty']:
                    valid_faculty = {field: faculty[field] for field in faculty_fields}
                    valid_faculty_data.append(valid_faculty)
                faculty_instances = [Faculty.objects.get_or_create(**faculty)[0] for faculty in valid_faculty_data]   
                # We are looping over the faculty twice. 
                # And we do it a third time for InstructorRoles below. However,
                # faculty_instances is a never large, only 1-3 per section.
                for faculty in faculty_instances:
                    faculty.program = program_instance
                    faculty.save()

                # Create MeetingTime instances
                meetingTime_instances = []
                meeting_time_data = data[key]['meetingsFaculty']
                for meeting_time in meeting_time_data:
                    valid_meeting_time = {field: meeting_time['meetingTime'][field] for field in meeting_time_fields}
                    meeting_time_instance = MeetingTime.objects.get_or_create(**valid_meeting_time)[0]
                    meetingTime_instances.append(meeting_time_instance)
                
                # Create MeetingLocation instances
                meetingLocation_instances = []
                meeting_location_data = data[key]['meetingsFaculty']
                for meeting_location in meeting_location_data:
                    valid_meeting_location = {field: meeting_location['meetingTime'][field] for field in meeting_location_fields}
                    meeting_location_instance = MeetingLocation.objects.get_or_create(**valid_meeting_location)[0]
                    meetingLocation_instances.append(meeting_location_instance)
                
                # Create Course instances
                valid_course_data = {field: data[key][field] for field in course_fields}
                valid_course_data.update({'program': program_instance})
                slug = slugify(valid_course_data['program'].subject + valid_course_data['courseNumber'])

                try:
                    course_instance = Course.objects.get(slug=slug)
                except Course.DoesNotExist:
                    course_instance = Course(**valid_course_data)
                    course_instance.save()

                # Create Section instances
                valid_section_data = {field: data[key][field] for field in section_fields}
                valid_section_data.update({'course': course_instance})
                section_instance = Section.objects.get_or_create(**valid_section_data)[0]
                
                section_instance.meetingLocation.add(*meetingLocation_instances)
                section_instance.meetingTime.add(*meetingTime_instances)

                # Create InstructorRole instances
                for i, faculty in enumerate(faculty_instances):
                    valid_instructor_role_data = {
                        'faculty': faculty,
                        'section': section_instance,
                        'primaryInstructor': data[key]['faculty'][i]['primaryIndicator']
                    }
                    instructor_role_instance = InstructorRole.objects.get_or_create(**valid_instructor_role_data)[0]