from django.urls import path
from .views import *

urlpatterns = [
    path('program/', GrandProgramList.as_view(), name='query_program'),
    path('program/<int:pk>/', GrandProgramDetail.as_view(), name='query_program'),
    path('programs/', ProgramList.as_view(), name='query_programs'),
    path('programs/<int:pk>/', ProgramDetail.as_view(), name='program_detail'),

    path('meetingtimes/', MeetingTimeList.as_view(), name='query_meeting_times'),
    path('meetingtimes/<int:pk>/', MeetingTimeDetail.as_view(), name='meeting_time_detail'),
    path('meetingtimes/<int:pk>/sections', MeetingTimeSections.as_view(), name='meeting_time_courses'),

    path('meetinglocations/', MeetingLocationList.as_view(), name='query_meeting_locations'),
    path('meetinglocations/<int:pk>/', MeetingLocationDetail.as_view(), name='meeting_location_detail'),
    path('meetinglocations/<int:pk>/sections', MeetingLocationSections.as_view(), name='meeting_location_courses'),

    path('courses/', CourseList.as_view(), name='query_courses'),
    path('courses/<int:pk>/', CourseDetail.as_view(), name='course_detail'),
    path('sections/', SectionList.as_view(), name='query_sections'),
    path('sections/<int:pk>/', SectionDetail.as_view(), name='section_detail'),
    
    path('degrees/', DegreeList.as_view(), name='query_degrees'),

    path('api/<str:term>/', TermCoursesView.as_view(), name='term_courses'),
    path('api/<str:term>/<str:subject>/', SubjectCoursesView.as_view(), name='subject_courses'),
    path('api/<str:term>/<str:subject>/<str:course_number>/', CourseSectionsView.as_view(), name='course_sections'),
    path('api/<str:term>/<str:subject>/<str:course_number>/<str:sequenceNumber>', DetailedSection.as_view(), name='course_sections')
]