import json
from django.core.management.base import BaseCommand
from django.template.defaultfilters import slugify
from courses.models import Degree, Section, MeetingTime, Course, Program, MeetingLocation, MeetingTime, CourseSectionLink

def bool_to_string(bool, day):
    if bool:
        case = {
            'monday': 'M',
            'tuesday': 'T',
            'wednesday': 'W',
            'thursday': 'Th',
            'friday': 'F',
            'saturday': 'S',
            'sunday': 'Su'
        }
        return case.get(day)
    else:
        return ''


class Command(BaseCommand):
    help = 'Load courses from JSON file into models'

    def add_arguments(self, parser):
        parser.add_argument('buildings', type=str, help='The JSON file to load courses from')
        parser.add_argument('courses', type=str, help='The JSON file to load courses from')
        parser.add_argument('degrees', type=str, help='The JSON file to load buildings from')

    def handle(self, *args, **options):
        '''Usage: python manage.py import_data data/*''' #then press TAB to autocomplete the filenames

        filename = options['buildings']
        with open(filename, 'r') as f:
            buildings = json.load(f)
        
        filename = options['degrees']
        with open(filename, 'r') as f:
            degrees = json.load(f)
            
        filename = options['courses']
        with open(filename, 'r') as f:
            courses = json.load(f)

            PROGRAMS = dict()
            MEETING_TIMES = dict()
            MEETING_LOCATIONS = dict()
            COURSES = dict()
            SECTIONS = []

            DEGREES = dict()
            SPECIALIZATIONS = dict()

            for course in courses.values():
                program_instance = Program(
                    subject_code=course['subject_code'],
                    subject=course['subject']
                )
                PROGRAMS[course['subject_code']] = program_instance

            for degree in degrees.values():
                if PROGRAMS.get(degree['subject']) is None:
                    program_instance = Program(
                        subject_code=degree['subject'],
                        subject=degree['subject']
                    )
                    PROGRAMS[degree['subject']] = program_instance

            Program.objects.bulk_create(list(PROGRAMS.values()))
            print("Programs loaded into db.")

            for course in courses.values():
                course_instance = Course(
                    slug = slugify(course['subject_code']+course['course_number']),
                    pid = course['pid'],
                    program=PROGRAMS[course['subject_code']],
                    course_number=course['course_number'],
                    title=course['title'],
                    credit=course.get('credit'),
                    description=course['description'],
                    notes=course.get('notes'),
                    link=course['link'],
                    hours=course.get('hours')
                )

                COURSES[course['pid']] = course_instance
                
                for sec in course['sections']:
                    for meet in sec['meetings']:
                        if meet.get('start') is None:
                            continue
                        meeting_time_identifier = meet.get('start')+'-'+meet.get('end')+ '-' +bool_to_string(meet.get('monday'), 'monday')+bool_to_string(meet.get('tuesday'), 'tuesday')+bool_to_string(meet.get('wednesday'), 'wednesday')+bool_to_string(meet.get('thursday'),'thursday')+bool_to_string(meet.get('friday'),'friday')+bool_to_string(meet.get('saturday'),'saturday')+bool_to_string(meet.get('sunday'),'sunday')

                        if MEETING_TIMES.get(meeting_time_identifier) is None:
                            meeting_time = MeetingTime(
                                slug=slugify(meeting_time_identifier),
                                term=sec['term'],
                                start=meet['start'],
                                end=meet['end'],
                                monday=meet['monday'],
                                tuesday=meet['tuesday'],
                                wednesday=meet['wednesday'],
                                thursday=meet['thursday'],
                                friday=meet['friday'],
                                saturday=meet['saturday'],
                                sunday=meet['sunday']
                            )
                            MEETING_TIMES[meeting_time_identifier] = meeting_time

                        if meet.get('building') is None or meet.get('room') is None:
                            continue

                        if sec['delivery'] == 'Online':
                            continue
                    
                        meeting_location_identifier = meet.get('building')+'-'+meet.get('room')

                        if MEETING_LOCATIONS.get(meeting_location_identifier) is None:
                            meeting_location = MeetingLocation(
                                slug=slugify(meeting_location_identifier),
                                building=meet['building'],
                                room=meet['room']
                            )
                            MEETING_LOCATIONS[meeting_location_identifier] = meeting_location

            MEETING_LOCATIONS['Online'] = MeetingLocation(
                slug='online',
                building='Online',
                room='Online'
            )
            MEETING_LOCATIONS['None'] = MeetingLocation(
                slug='none',
                building='None',
                room='None'
            )
            Course.objects.bulk_create(list(COURSES.values()))
            MeetingTime.objects.bulk_create(list(MEETING_TIMES.values()))
            MeetingLocation.objects.bulk_create(list(MEETING_LOCATIONS.values()))
            print("Courses and meetings loaded into db.")

            for course in courses.values():
                course_instance = COURSES[course['pid']]
                for sec in course['sections']:
                    if len(sec['meetings']) == 0:
                        # some random exchange law courses has no meetings lol.
                        continue
                    if sec['campus'] == 'Online':
                        meeting_location_identifier = 'Online'
                        
                    elif sec['meetings'][0].get('building') is None or sec['meetings'][0].get('room') is None:
                            meeting_location_identifier = 'None'
                    else:
                        meeting_time_identifier = meet.get('start')+'-'+meet.get('end')+ '-' +bool_to_string(meet.get('monday'), 'monday')+bool_to_string(meet.get('tuesday'), 'tuesday')+bool_to_string(meet.get('wednesday'), 'wednesday')+bool_to_string(meet.get('thursday'),'thursday')+bool_to_string(meet.get('friday'),'friday')+bool_to_string(meet.get('saturday'),'saturday')+bool_to_string(meet.get('sunday'),'sunday')
                        meeting_location_identifier = sec['meetings'][0].get('building')+'-'+sec['meetings'][0].get('room')
                    
                    section_instance = Section(
                        course=course_instance,
                        sequence=sec['sequence'],
                        crn=sec['crn'],
                        meeting_time=MEETING_TIMES[meeting_time_identifier],
                        meeting_location=MEETING_LOCATIONS[meeting_location_identifier],
                        term=sec['term'],
                        credit=sec['credit'],
                        type=sec['type'],
                        delivery=sec['delivery'],
                    )
                    SECTIONS.append(section_instance)
            Section.objects.bulk_create(SECTIONS)
            print("Sections loaded into db.")

            for degree in degrees.values():
                
                degree_instance = Degree(
                    code=degree['code'],
                    cred=degree['type'],
                    program=PROGRAMS[degree['subject']],
                    description=degree['description'],
                    link=degree['link'],
                    notes=degree['notes'],
                    requirements=degree['requirements']
                )
                DEGREES[degree['code']] = degree_instance

            Degree.objects.bulk_create(list(DEGREES.values()))
            print("Degrees loaded into db.")

            self.stdout.write(self.style.SUCCESS('\nLoaded all courses into db.\n'))
