from .models import *
from .serializers import *
from django.db.models import Q
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    
    context = {
        # You can pass context data to your template here
        'course_name': 'Sample Course',
        'course': 'This is a sample course description.',
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

        queryset = Program.objects.all().order_by('subject')
        
        subject_code = self.request.query_params.get('subject')
        if subject_code:
            queryset = queryset.filter(subject_code__icontains=subject_code)

        subj = self.request.query_params.get('subject_desc')
        if subj:
            queryset = queryset.filter(subject__icontains=subj)

        return queryset
    
class ProgramDetail(generics.RetrieveAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    serializer_class = CourseSectionSerializer
    def get_queryset(self):
        return Section.objects.order_by('course__program__subject', 'course__course_number', 'sequence')

class MeetingTimeList(generics.ListAPIView):
    serializer_class = MeetingTimeSerializer
    pagination_class = PageNumberPagination
    def get_queryset(self):

        queryset = MeetingTime.objects.all().order_by('term', 'start', 'end')

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

        # bldg = self.request.query_params.get('bldg')
        # if bldg:
        #     queryset = queryset.filter(sections__meetingLocation__buildingDescription__icontains=bldg).distinct()

        start = self.request.query_params.get('start')
        if start:
            queryset = queryset.filter(start=start)

    
        end = self.request.query_params.get('end')
        if end:
            queryset = queryset.filter(end=end)
        
        saft = self.request.query_params.get('saft')
        if saft:
            queryset = queryset.filter(start__gte=saft)
        
        ebef = self.request.query_params.get('ebef')
        if ebef:
            queryset = queryset.filter(end__lte=ebef)

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
        queryset = MeetingLocation.objects.all().order_by('building', 'room')

        building = self.request.query_params.get('bldg')
        if building:
            queryset = queryset.filter(building__icontains=building)

        wing = self.request.query_params.get('wing')
        if wing:
            queryset = queryset.filter(room__startswith=wing)

        # subject = self.request.query_params.get('subject')
        # if subject:
        #     queryset = queryset.filter(sections__course__program__subject=subject).distinct()

        return queryset

class MeetingLocationDetail(generics.RetrieveAPIView):
    queryset = MeetingLocation.objects.all()
    serializer_class = MeetingLocationSerializer

class MeetingLocationSections(generics.ListAPIView):
    serializer_class = CourseSerializer
    pagination_class = PageNumberPagination
    def get_queryset(self):
        meeting_location = MeetingLocation.objects.get(id=self.kwargs['pk'])
        queryset = Course.objects.filter(sections__meeting_location=meeting_location)

        subject = self.request.query_params.get('subject')
        if subject:
            queryset = queryset.filter(program__subject=subject)

        return queryset

class CourseList(generics.ListAPIView):
    serializer_class = CourseSerializer
    pagination_class = PageNumberPagination
    def get_queryset(self):
        queryset = Course.objects.order_by('program__subject', 'course_number')

        subject = self.request.query_params.get('subject')
        if subject:
            queryset = queryset.filter(program__subject__icontains=subject)

        bldg = self.request.query_params.get('bldg')
        if bldg:
            queryset = queryset.filter(sections__meeting_location__building__icontains=bldg)

        building = self.request.query_params.get('bldg')
        if building:
            queryset = queryset.filter(sections__meeting_location__building__icontains=building)

        level = self.request.query_params.get('level')
        if level:
            queryset = queryset.filter(course_number__startswith=level)

        title = self.request.query_params.get('title')
        if title:
            queryset = queryset.filter(title__icontains=title)

        credits = self.request.query_params.get('credits')
        if credits:
            queryset = queryset.filter(credit=credits)

        return queryset
    
class CourseDetail(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class SectionList(generics.ListAPIView):
    serializer_class = SectionSerializer
    pagination_class = PageNumberPagination
    def get_queryset(self):
        queryset = Section.objects.order_by('course__program__subject', 'course__course_number')

        subject = self.request.query_params.get('subject')
        if subject:
            queryset = queryset.filter(course__program__subject=subject)

        course = self.request.query_params.get('course')
        if course:
            queryset = queryset.filter(course__course_number=course)
        
        term = self.request.query_params.get('term')
        if term:
            queryset = queryset.filter(term=term)

        # Allow partial matches for building description
        building = self.request.query_params.get('bldg')
        if building:
            queryset = queryset.filter(meeting_location__building__icontains=building)

        room = self.request.query_params.get('room')
        if room:
            queryset = queryset.filter(meeting_location__room=room)

        crn = self.request.query_params.get('crn')
        if crn:
            queryset = queryset.filter(crn=crn)

        delivery = self.request.query_params.get('delivery')
        if delivery:
            queryset = queryset.filter(meeting_time__delivery=delivery)
        
        course_type = self.request.query_params.get('type')
        if course_type:
            queryset = queryset.filter(type__icontains=course_type)

        # Filter by days strictly (all days must be true)
        days_of_week = self.request.query_params.get('on')
        if days_of_week:
            days_dict = get_days_of_week(days_of_week)
            filter_query = Q()
            for day, value in days_dict.items():
                if value == 1:
                    filter_name = f'meeting_time__{day}'
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
                    filter_name = f'meeting_time__{day}'
                    filter_query |= Q(**{filter_name: True})
            queryset = queryset.filter(filter_query)

        begin = self.request.query_params.get('begin')
        if begin:
            queryset = queryset.filter(meeting_time__start=begin)

        end = self.request.query_params.get('end')
        if end:
            queryset = queryset.filter(meeting_time__end=end)
        
        bAfter = self.request.query_params.get('baft')
        if bAfter:
            queryset = queryset.filter(meeting_time__start__gte=bAfter)
        
        eBefore = self.request.query_params.get('ebef')
        if eBefore:
            queryset = queryset.filter(meeting_time__end__lte=eBefore)

        return queryset

class SectionDetail(generics.RetrieveAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer

class DegreeList(generics.ListAPIView):
    serializer_class = DegreeSerializer
    pagination_class = PageNumberPagination
    def get_queryset(self):
        queryset = Degree.objects.all().order_by('program__subject', 'cred')

        subject = self.request.query_params.get('subject')
        if subject:
            queryset = queryset.filter(program__subject=subject)

        cred = self.request.query_params.get('cred')
        if cred:
            queryset = queryset.filter(cred=cred)

        code = self.request.query_params.get('code')
        if code:
            queryset = queryset.filter(code=code)

        return queryset

class GrandProgramList(generics.ListAPIView):
    serializer_class = GrandProgramSerializer
    pagination_class = PageNumberPagination
    def get_queryset(self):
        queryset = Program.objects.all().order_by('subject')

        subject = self.request.query_params.get('subject')
        if subject:
            queryset = queryset.filter(subject=subject)

        return queryset

class GrandProgramDetail(generics.RetrieveAPIView):
    queryset = Program.objects.all()
    serializer_class = GrandProgramSerializer
        
class TermCoursesView(APIView, PageNumberPagination):
    def get(self, request, term, format=None):
        courses = Course.objects.filter(term=term).order_by('program__subject','course_number')
        page = self.paginate_queryset(courses, request)
        serializer = CourseSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

class SubjectCoursesView(APIView):
    def get(self, request, term, subject, format=None):
        courses = Course.objects.filter(term=term, program__subject=subject).order_by('course_number')
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CourseSectionsView(APIView):
    def get(self, request, term, subject, course_number, format=None):
        sections = Section.objects.filter(term=term, course__program__subject=subject, course__course_number=course_number).order_by('sequenceNumber')
        serializer = BriefSectionSerializer(sections, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class DetailedSection(APIView):
    def get(self, request, term, subject, course_number, sequence, format=None):
        section = Section.objects.get(term=term, course__program__subject=subject, course__course_number=course_number, sequence=sequence)
        serializer = SectionSerializer(section)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

