from django.db import models
from Administrator.models import Pupil, ClassRoom, Users

# Create your models here.
class Attendance(models.Model):
    """
    Holds the Attendance Records
    """
    pupil = models.ForeignKey(Pupil, on_delete=models.CASCADE, blank=False, null=True)
    is_present = models.BooleanField(default=False) # true if pupil is present
    day = models.DateField()
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, blank=False, null=True)
    teacher = models.ForeignKey(Users, on_delete=models.CASCADE, blank=False, null=True)