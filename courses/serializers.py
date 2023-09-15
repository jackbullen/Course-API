from rest_framework import serializers
from .models import *

class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = '__all__'

class MeetingTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingTime
        fields = '__all__'

class MeetingLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingLocation
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    program = ProgramSerializer()
    class Meta:
        model = Course
        fields = '__all__'
    
class SectionSerializer(serializers.ModelSerializer):
    # meeting_time = MeetingTimeSerializer() 
    # meeting_location = MeetingLocationSerializer()
    # course = CourseSerializer()
    # instructors = InstructorRoleSerializer(many=True)
    class Meta:
        model = Section
        fields = '__all__'

class BriefSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = '__all__'

class CourseSectionSerializer(serializers.ModelSerializer):
    course = CourseSerializer()
    class Meta:
        model = Section
        fields = '__all__'

class DegreeSerializer(serializers.ModelSerializer):
    program = ProgramSerializer()
    class Meta:
        model = Degree
        fields = '__all__'

class BriefDegreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Degree
        fields = '__all__'

class GrandProgramSerializer(serializers.ModelSerializer):
    degrees = BriefDegreeSerializer(many=True)
    courses = CourseSerializer(many=True)
    class Meta:
        model = Program
        fields = '__all__'

class APISerializer(serializers.Serializer):
    subject = serializers.CharField(required=False)
    course = serializers.CharField(required=False)
    term = serializers.CharField(required=False)
    bldg = serializers.CharField(required=False)
    room = serializers.CharField(required=False)
    F2F = serializers.CharField(required=False)
    type = serializers.CharField(required=False)
