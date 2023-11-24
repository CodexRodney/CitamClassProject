from django.db import models

# Create your models here.
class Event(models.Model):
    """
    Used to hold information about the DBVMS event
    """
    parent_email = models.EmailField(unique=True)
    parent_name = models.CharField(max_length=100, blank=False)
    parent_phone_number = models.CharField(max_length=100, blank=False, unique=True)
    children = models.CharField(max_length=1000, blank=False)
    need_tranport = models.BooleanField(default=False) # true if Kids need transport
    parent_location = models.CharField(max_length=100)
    prnt_cfrm_pickup = models.DateTimeField()
    tchr_cfrm_received = models.DateTimeField()
    tchr_cfrm_released = models.DateTimeField()
    prnt_cfrm_dropped = models.DateTimeField()
    dbvms_year = models.IntegerField(null=True, blank=False)