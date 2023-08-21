from django.contrib import admin
from .models import Faculty, Course, MeetingTime, MeetingLocation, Program, Section, InstructorRole, CourseLabLink, CourseTutorialLink

class FacultyAdmin(admin.ModelAdmin):
    list_display = ('displayName', 'emailAddress')
    search_fields = ('displayName','bannerId')

class CourseAdmin(admin.ModelAdmin):
    list_display = ('program', 'courseNumber', 'courseTitle', 'term', 'creditHours')
    search_fields = ('program', 'courseNumber', 'courseTitle', 'term')

class MeetingTimeAdmin(admin.ModelAdmin):
    list_display = ('term', 'beginTime', 'endTime', 'startDate', 'endDate')
    search_fields = ('term', 'beginTime', 'endTime', 'startDate', 'endDate')

class MeetingLocationAdmin(admin.ModelAdmin):
    list_display = ('buildingDescription', 'room')
    search_fields = ('buildingDescription', 'room')

class ProgramAdmin(admin.ModelAdmin):
    list_display = ('subject', 'subjectDescription')
    search_fields = ('subject', 'subjectDescription')

class SectionAdmin(admin.ModelAdmin):
    list_display = ('course','sequenceNumber',  'courseReferenceNumber', 'term', 'scheduleTypeDescription', 'seatsAvailable')
    search_fields = ('course', 'sequenceNumber', 'courseReferenceNumber', 'term', 'scheduleTypeDescription', 'instructionalMethod')

class InstructorRoleAdmin(admin.ModelAdmin):
    list_display = ('section', 'faculty', 'primaryInstructor')
    search_fields = ('section', 'faculty')

admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(MeetingTime, MeetingTimeAdmin)
admin.site.register(MeetingLocation, MeetingLocationAdmin)
admin.site.register(Program, ProgramAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(InstructorRole, InstructorRoleAdmin)
admin.site.register(CourseLabLink)
admin.site.register(CourseTutorialLink)