from django.db import models
from django.template.defaultfilters import slugify

# Program, Faculty, MeetingTime and MeetingLocation, Course, Section, Degree, and Specialization

class Program(models.Model):
    subject_code = models.CharField(max_length=10, unique=True, primary_key=True)
    subject = models.CharField(max_length=100)
    def __str__(self):
        return self.subject

class MeetingTime(models.Model):
    slug = models.SlugField(max_length=200, unique=True, primary_key=True)
    term = models.CharField(max_length=6)
    start = models.CharField(max_length=6, null=True)
    end = models.CharField(max_length=6, null=True)
    monday = models.BooleanField(default=False)
    tuesday = models.BooleanField(default=False)
    wednesday = models.BooleanField(default=False)
    thursday = models.BooleanField(default=False)
    friday = models.BooleanField(default=False)
    saturday = models.BooleanField(default=False)
    sunday = models.BooleanField(default=False)
    # strInfo = models.CharField(max_length=5, null=True) # something like "MTh" or "TWF"
    def __str__(self):
        return f"{self.term} {self.start}-{self.end}"
    
class MeetingLocation(models.Model):
    slug = models.SlugField(max_length=200, unique=True, primary_key=True)
    building = models.CharField(max_length=100, null=True)
    room = models.CharField(max_length=10, null=True)
    # latitute = models.CharField(max_length=20, null=True)
    # longitude = models.CharField(max_length=20, null=True)
    def __str__(self):
        return f"{self.building} {self.room}"

class Course(models.Model):
    pid = models.CharField(max_length=30, unique=True, primary_key=True)
    slug = models.SlugField(max_length=200, unique=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='courses')
    course_number = models.CharField(max_length=100) #370
    title = models.CharField(max_length=200) #Database Systems
    credit = models.CharField(max_length=100, null=True)
    hours = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=15000, null=True)
    notes = models.CharField(max_length=10000, null=True)
    link = models.CharField(max_length=200, null=True)
    def __str__(self):
        return f"{self.program}{self.course_number}"

# class CourseReview(models.Model):
#     course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
#     rating = models.CharField(max_length=10)
#     review = models.CharField(max_length=10000)
#     def __str__(self):
#         return f"{self.course} - {self.rating}"
    
class Section(models.Model):
    term = models.CharField(max_length=6)
    crn = models.CharField(max_length=10, unique=True, primary_key=True)
    sequence = models.CharField(max_length=10) #A01
    type = models.CharField(max_length=100) #Lecture
    delivery = models.CharField(max_length=10) #F2F
    credit = models.CharField(max_length=10) 
    meeting_time = models.ForeignKey(MeetingTime, on_delete=models.CASCADE, related_name='sections')
    meeting_location = models.ForeignKey(MeetingLocation, on_delete=models.CASCADE, related_name='sections')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sections')
    def __str__(self):
        return f"{self.sequenceNumber}"
    
class Degree(models.Model):
    code = models.CharField(max_length=100, unique=True, primary_key=True)
    cred = models.CharField(max_length=100)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='degrees', null=True) 
    description = models.CharField(max_length=10000, null=True)
    link = models.CharField(max_length=200, null=True)
    requirements = models.CharField(max_length=50000, null=True)
    notes = models.CharField(max_length=10000, null=True)
    def __str__(self):
        return self.code

class Specialization(models.Model):
    degree = models.ForeignKey(Degree, on_delete=models.CASCADE, related_name='specializations')
    requirements = models.CharField(max_length=30000, null=True)
    title = models.CharField(max_length=100)
    notes = models.CharField(max_length=10000, null=True)
    def __str__(self):
        return self.degree.program.subject + " - " + self.degree.cred + " - " + self.title
    
# For models like InstructorRole and CourseSectionLink should I be using ForeignKey or ManyToManyField?
# Create a bunch more objects or just make one and handle all links through there.
# or add field to sections model and handle that way.
# Having only fields would speed up, but can make map with time/location objects.
    
# Just make two objects for each course and have ManyToManyField for each section.
class CourseSectionLink(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='linked_sections')
    sections = models.ManyToManyField(Section, related_name='linked_sections')
    type = models.CharField(max_length=10)
    def __str__(self):
        return f"{self.course} - {self.sections}"