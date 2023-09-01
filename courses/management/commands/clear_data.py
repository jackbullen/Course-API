from django.core.management.base import BaseCommand
from courses.models import *

class Command(BaseCommand):
    help = 'Clear all data from YourModel'

    def handle(self, *args, **kwargs):
        Course.objects.all().delete()
        Program.objects.all().delete()
        Faculty.objects.all().delete()
        MeetingTime.objects.all().delete()
        MeetingLocation.objects.all().delete()
        Section.objects.all().delete()
        InstructorRole.objects.all().delete()
        CourseSectionLink.objects.all().delete()
        Degree.objects.all().delete()
        Specialization.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Cleared all data from database.'))
