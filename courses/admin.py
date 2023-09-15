# from django.contrib import admin
# from .models import Faculty, Course, MeetingTime, MeetingLocation, Program, Section, InstructorRole, CourseSectionLink, Degree, Specialization

# class FacultyAdmin(admin.ModelAdmin):
#     list_display = ('displayName', 'emailAddress')
#     search_fields = ('displayName','bannerId')

# class CourseAdmin(admin.ModelAdmin):
#     list_display = ('program', 'course_number', 'title', 'credit')
#     search_fields = ('program', 'course_number', 'title')

# class MeetingTimeAdmin(admin.ModelAdmin):
#     list_display = ('term', 'beginTime', 'endTime', 'startDate', 'endDate')
#     search_fields = ('term', 'beginTime', 'endTime', 'startDate', 'endDate')

# class MeetingLocationAdmin(admin.ModelAdmin):
#     list_display = ('buildingDescription', 'room')
#     search_fields = ('buildingDescription', 'room')

# class ProgramAdmin(admin.ModelAdmin):
#     list_display = ('subject_code', 'subject')
#     search_fields = ('subject_code', 'subject')

# class SectionAdmin(admin.ModelAdmin):
#     list_display = ('course','sequenceNumber',  'courseReferenceNumber', 'term', 'scheduleTypeDescription', 'seatsAvailable')
#     search_fields = ('course', 'sequenceNumber', 'courseReferenceNumber', 'term', 'scheduleTypeDescription', 'instructionalMethod')

# class InstructorRoleAdmin(admin.ModelAdmin):
#     list_display = ('section', 'faculty', 'primaryInstructor')
#     search_fields = ('section', 'faculty')

# class CourseSectionLinkAdmin(admin.ModelAdmin):
#     list_display = ('course', 'section')
#     search_fields = ('course', 'section')

# class DegreeAdmin(admin.ModelAdmin):
#     list_display = ('code', 'cred', 'program')
#     search_fields = ('code', 'cred', 'program')

# # class SpecializationAdmin(admin.ModelAdmin):
    


# admin.site.register(Faculty, FacultyAdmin)
# admin.site.register(Course, CourseAdmin)
# admin.site.register(MeetingTime, MeetingTimeAdmin)
# admin.site.register(MeetingLocation, MeetingLocationAdmin)
# admin.site.register(Program, ProgramAdmin)
# admin.site.register(Section, SectionAdmin)
# admin.site.register(InstructorRole, InstructorRoleAdmin)
# admin.site.register(CourseSectionLink)
# admin.site.register(Degree, DegreeAdmin)
# admin.site.register(Specialization)
