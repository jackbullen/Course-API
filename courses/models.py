from django.db import models
from django.template.defaultfilters import slugify

# Program, Faculty, MeetingTime and MeetingLocation, Course, Section, Degree, and Specialization

class Program(models.Model):
    subject = models.CharField(max_length=10, unique=True)
    subjectDescription = models.CharField(max_length=100)
    def __str__(self):
        return self.subject

class Faculty(models.Model):
    bannerId = models.CharField(max_length=10) 
    displayName = models.CharField(max_length=100)
    emailAddress = models.EmailField()
    program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True, related_name='faculty_members')
    def __str__(self):
        return self.displayName

class MeetingTime(models.Model):
    term = models.CharField(max_length=6)
    beginTime = models.CharField(max_length=6, null=True)
    endTime = models.CharField(max_length=6, null=True)
    startDate = models.CharField(max_length=15)
    endDate = models.CharField(max_length=15)
    monday = models.BooleanField(default=False)
    tuesday = models.BooleanField(default=False)
    wednesday = models.BooleanField(default=False)
    thursday = models.BooleanField(default=False)
    friday = models.BooleanField(default=False)
    saturday = models.BooleanField(default=False)
    sunday = models.BooleanField(default=False)
    # strInfo = models.CharField(max_length=5, null=True) # something like "MTh" or "TWF"
    def __str__(self):
        return f"{self.term} {self.beginTime}-{self.endTime}"
    
class MeetingLocation(models.Model):
    building = models.CharField(max_length=20, null=True)
    buildingDescription = models.CharField(max_length=100, null=True)
    room = models.CharField(max_length=10, null=True)
    campus = models.CharField(max_length=10, null=True)
    campusDescription = models.CharField(max_length=100, null=True)
    # latitute = models.CharField(max_length=20, null=True)
    # longitude = models.CharField(max_length=20, null=True)
    def __str__(self):
        return f"{self.building} {self.room} ({self.campus})"

class Course(models.Model):
    term = models.CharField(max_length=6, null=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, null=True, related_name='courses')
    courseNumber = models.CharField(max_length=10) #370
    courseTitle = models.CharField(max_length=200) #Database Systems
    slug = models.SlugField(max_length=200, unique=True)
    creditHours = models.CharField(max_length=10, null=True)
    description = models.CharField(max_length=15000, null=True)
    link = models.CharField(max_length=200, null=True)
    def __str__(self):
        return f"{self.program}{self.courseNumber} - {self.term}"
    def save(self, *args, **kwargs):
        ct = Course.objects.all().count()
        self.slug = slugify(self.program.subject+self.courseNumber+'-'+self.term)
        super(Course, self).save(*args, **kwargs)

# class CourseReview(models.Model):
#     course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
#     rating = models.CharField(max_length=10)
#     review = models.CharField(max_length=10000)
#     def __str__(self):
#         return f"{self.course} - {self.rating}"
    
class Section(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    term = models.CharField(max_length=6)
    courseReferenceNumber = models.CharField(max_length=10)
    sequenceNumber = models.CharField(max_length=10) #A01
    scheduleTypeDescription = models.CharField(max_length=100) #Lecture
    instructionalMethod = models.CharField(max_length=10) #F2F
    meetingTime = models.ManyToManyField(MeetingTime, related_name='sections')
    meetingLocation = models.ManyToManyField(MeetingLocation, related_name='sections')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sections')
    maximumEnrollment = models.CharField(max_length=10)
    enrollment = models.CharField(max_length=10)
    seatsAvailable = models.CharField(max_length=10)
    waitCapacity = models.CharField(max_length=10)
    waitCount = models.CharField(max_length=10)
    waitAvailable = models.CharField(max_length=10)
    def __str__(self):
        return f"{self.sequenceNumber}"
    
class Degree(models.Model):
    code = models.CharField(max_length=100, unique=True)
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

# Create a bunch of objects for each section/faculty pair.
class InstructorRole(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='instructors')
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='instructing')
    primaryInstructor = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.faculty} - {self.section}"
    
# Just make two objects for each course and have ManyToManyField for each section.
class CourseSectionLink(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='linked_sections')
    sections = models.ManyToManyField(Section, related_name='linked_sections')
    type = models.CharField(max_length=10)
    def __str__(self):
        return f"{self.course} - {self.sections}"