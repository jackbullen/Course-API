from .models import *
from .serializers import *
from django.db.models import Q
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    
    context = {
        # You can pass context data to your template here
        'course_name': 'Sample Course',
        'course_description': 'This is a sample course description.',
    }

    return render(request, 'courses/courses.html', context)

def get_days_of_week(days_of_week_string):
    '''
    Converts a string of 7 1s and 0s to a dictionary of days of the week.
    Used to filter objects by days of the week.
    '''
    days_dict = {
                'monday': int(days_of_week_string[0]),
                'tuesday': int(days_of_week_string[1]),
                'wednesday': int(days_of_week_string[2]),
                'thursday': int(days_of_week_string[3]),
                'friday': int(days_of_week_string[4]),
                'saturday': int(days_of_week_string[5]),
                'sunday': int(days_of_week_string[6])
            }
    return days_dict

class ProgramList(generics.ListAPIView):
    serializer_class = ProgramSerializer
    def get_queryset(self):
        return Program.objects.all().order_by('subject')
    
class ProgramDetail(generics.RetrieveAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer

class FacultyList(generics.ListAPIView):
    serializer_class = FacultySerializer
    def get_queryset(self):

        queryset = Faculty.objects.all().order_by('displayName')

        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(displayName__icontains=name)

        program = self.request.query_params.get('program')
        if program:
            queryset = queryset.filter(programs__subject=program)

        courseReferenceNumber = self.request.query_params.get('refnum')
        if courseReferenceNumber:
            print()
            queryset = queryset.filter(instructing__section__courseReferenceNumber=courseReferenceNumber)

        return queryset
    
class FacultyDetail(generics.RetrieveAPIView):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer

class FacultySections(generics.ListAPIView):
    serializer_class = CourseSectionSerializer
    def get_queryset(self):
        faculty_id = self.kwargs['pk']
        return Section.objects.filter(instructors=faculty_id).order_by('course__program__subject', 'course__courseNumber', 'sequenceNumber')

class MeetingTimeList(generics.ListAPIView):
    serializer_class = MeetingTimeSerializer
    pagination_class = PageNumberPagination
    def get_queryset(self):

        queryset = MeetingTime.objects.all().order_by('term', 'beginTime', 'endTime')

        # Filter by days strictly (all days must be true)
        days_of_week = self.request.query_params.get('on')
        if days_of_week:
            days_dict = get_days_of_week(days_of_week)
            filter_query = Q()
            for day, value in days_dict.items():
                if value == 1:
                    filter_query &= Q(**{day: True})
                else:
                    filter_query &= Q(**{day: False})
            queryset = queryset.filter(filter_query)

        # Filter by days loosely (one of the days is true)
        days = self.request.query_params.get('days')
        if days:
            days_dict = get_days_of_week(days)
            filter_query = Q()
            for day, value in days_dict.items():
                if value==1:
                    filter_query |= Q(**{day: True})
            queryset = queryset.filter(filter_query)

        bldg = self.request.query_params.get('bldg')
        if bldg:
            queryset = queryset.filter(sections__meetingLocation__buildingDescription__icontains=bldg).distinct()

        start = self.request.query_params.get('start')
        if start:
            queryset = queryset.filter(beginTime=start)

    
        end = self.request.query_params.get('end')
        if end:
            queryset = queryset.filter(endTime=end)
        
        saft = self.request.query_params.get('saft')
        if saft:
            queryset = queryset.filter(beginTime__gte=saft)
        
        ebef = self.request.query_params.get('ebef')
        if ebef:
            queryset = queryset.filter(endTime__lte=ebef)

        return queryset

class MeetingTimeDetail(generics.RetrieveAPIView):
    queryset = MeetingTime.objects.all()
    serializer_class = MeetingTimeSerializer

class MeetingTimeSections(generics.ListAPIView):
    serializer_class = CourseSerializer
    pagination_class = PageNumberPagination
    def get_queryset(self):
        meeting_time = MeetingTime.objects.get(id=self.kwargs['pk'])
        queryset = Course.objects.filter(sections__meetingTime=meeting_time)

        subject = self.request.query_params.get('subject')
        if subject:
            queryset = queryset.filter(program__subject=subject)
        
        return queryset

class MeetingLocationList(generics.ListAPIView):
    serializer_class = MeetingLocationSerializer
    def get_queryset(self):
        queryset = MeetingLocation.objects.all().order_by('building', 'room', 'campus')

        building_description = self.request.query_params.get('bldg')
        if building_description:
            queryset = queryset.filter(buildingDescription__icontains=building_description)

        wing = self.request.query_params.get('wing')
        if wing:
            queryset = queryset.filter(room__startswith=wing)

        subject = self.request.query_params.get('subject')
        if subject:
            queryset = queryset.filter(sections__course__program__subject=subject).distinct()

        return queryset

class MeetingLocationDetail(generics.RetrieveAPIView):
    queryset = MeetingLocation.objects.all()
    serializer_class = MeetingLocationSerializer

class MeetingLocationSections(generics.ListAPIView):
    serializer_class = CourseSerializer
    pagination_class = PageNumberPagination
    def get_queryset(self):
        meeting_location = MeetingLocation.objects.get(id=self.kwargs['pk'])
        queryset = Course.objects.filter(sections__meetingLocation=meeting_location)

        subject = self.request.query_params.get('subject')
        if subject:
            queryset = queryset.filter(program__subject=subject)

        return queryset

class CourseList(generics.ListAPIView):
    serializer_class = CourseSerializer
    pagination_class = PageNumberPagination
    def get_queryset(self):
        queryset = Course.objects.order_by('program__subject', 'courseNumber')

        subject = self.request.query_params.get('subject')
        if subject:
            queryset = queryset.filter(program__subject=subject)

        bldg = self.request.query_params.get('bldg')
        if bldg:
            queryset = queryset.filter(sections__meetingLocation__buildingDescription__icontains=bldg)

        term = self.request.query_params.get('term')
        if term:
            queryset = queryset.filter(term=term)

        building_description = self.request.query_params.get('bldg')
        if building_description:
            queryset = queryset.filter(sections__meetingLocation__buildingDescription__icontains=building_description)

        level = self.request.query_params.get('level')
        if level:
            queryset = queryset.filter(courseNumber__startswith=level)

        title = self.request.query_params.get('title')
        if title:
            queryset = queryset.filter(courseTitle__icontains=title)

        credits = self.request.query_params.get('credits')
        if credits:
            queryset = queryset.filter(creditHours=credits)

        refnum = self.request.query_params.get('refnum')
        if refnum:
            queryset = queryset.filter(referenceNumber=refnum)

        return queryset
    
class CourseDetail(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class SectionList(generics.ListAPIView):
    serializer_class = SectionSerializer
    pagination_class = PageNumberPagination
    def get_queryset(self):
        queryset = Section.objects.order_by('course__program__subject', 'course__courseNumber')

        subject = self.request.query_params.get('subject')
        if subject:
            queryset = queryset.filter(course__program__subject=subject)

        course = self.request.query_params.get('course')
        if course:
            queryset = queryset.filter(course__courseNumber=course)
        
        term = self.request.query_params.get('term')
        if term:
            queryset = queryset.filter(term=term)

        # Allow partial matches for building description
        building_description = self.request.query_params.get('bldg')
        if building_description:
            queryset = queryset.filter(meetingLocation__buildingDescription__icontains=building_description)

        room = self.request.query_params.get('room')
        if room:
            queryset = queryset.filter(meetingLocation__room=room)

        refnum = self.request.query_params.get('refnum')
        if refnum:
            queryset = queryset.filter(courseReferenceNumber=refnum)

        instructional_method = self.request.query_params.get('F2F')
        if instructional_method:
            queryset = queryset.filter(meetingTime__instructionalMethod=instructional_method)
        
        course_type = self.request.query_params.get('type')
        if course_type:
            queryset = queryset.filter(scheduleTypeDescription__icontains=course_type)

        # Filter by days strictly (all days must be true)
        days_of_week = self.request.query_params.get('on')
        if days_of_week:
            days_dict = get_days_of_week(days_of_week)
            filter_query = Q()
            for day, value in days_dict.items():
                if value == 1:
                    filter_name = f'meetingTime__{day}'
                    filter_query &= Q(**{filter_name: True})
                else:
                    filter_query &= Q(**{day: False})
            queryset = queryset.filter(filter_query)

        # Filter by days loosely (one of the days is true)
        days = self.request.query_params.get('days')
        if days:
            days_dict = get_days_of_week(days)
            filter_query = Q()
            for day, value in days_dict.items():
                if value==1:
                    filter_name = f'meetingTime__{day}'
                    filter_query |= Q(**{filter_name: True})
            queryset = queryset.filter(filter_query)

        begin = self.request.query_params.get('begin')
        if begin:
            queryset = queryset.filter(meetingTime__beginTime=begin)

        end = self.request.query_params.get('end')
        if end:
            queryset = queryset.filter(meetingTime__endTime=end)
        
        bAfter = self.request.query_params.get('baft')
        if bAfter:
            queryset = queryset.filter(meetingTime__beginTime__gte=bAfter)
        
        eBefore = self.request.query_params.get('ebef')
        if eBefore:
            queryset = queryset.filter(meetingTime__endTime__lte=eBefore)

        return queryset

class SectionDetail(generics.RetrieveAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer

class TermCoursesView(APIView):
    def get(self, request, term, format=None):
        courses = Course.objects.filter(term=term).order_by('program__subject','courseNumber')
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SubjectCoursesView(APIView):
    def get(self, request, term, subject, format=None):
        courses = Course.objects.filter(term=term, program__subject=subject).order_by('courseNumber')
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CourseSectionsView(APIView):
    def get(self, request, term, subject, course_number, format=None):
        sections = Section.objects.filter(term=term, course__program__subject=subject, course__courseNumber=course_number).order_by('sequenceNumber')
        serializer = BriefSectionSerializer(sections, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class DetailedSection(APIView):
    def get(self, request, term, subject, course_number, sequenceNumber, format=None):
        section = Section.objects.get(term=term, course__program__subject=subject, course__courseNumber=course_number, sequenceNumber=sequenceNumber)
        serializer = SectionSerializer(section)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

