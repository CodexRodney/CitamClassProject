from django.db import models
from Administrator.models import Users

# Create your models here.
grades = (
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
    ("6", "6"),
    ("7", "7"),
    ("8", "8"),
)

class Event(models.Model):
    """
    Used to hold information about the DBVMS event
    """
    parent_email = models.EmailField(unique=True)
    parent_name = models.CharField(max_length=100, blank=False)
    parent_phone_number = models.CharField(max_length=100, blank=False, unique=True)
    pupil = models.CharField(max_length=1000, blank=False)
    need_tranport = models.BooleanField(default=False) # true if Kids need transport
    parent_location = models.CharField(max_length=100)
    prnt_cfrm_pickup = models.DateTimeField()
    tchr_cfrm_received = models.DateTimeField()
    tchr_cfrm_released = models.DateTimeField()
    prnt_cfrm_dropped = models.DateTimeField()
    dbvms_year = models.IntegerField(null=True, blank=False)
    teacher_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    grade = models.CharField(max_length=5, choices=grades, blank=False, null=True)