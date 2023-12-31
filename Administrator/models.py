# Create your models here.
from datetime import date, datetime
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.db import models

gender = (
    ("male", "male"),
    ("female", "female"),
    )

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

roles = (
    ("teacher", "teacher"),
    ("admin", "admin"),
    ("parent", "parent"),
    ("driver", "driver"),
)

class Users(AbstractBaseUser):
    """
    This is the Administrator table:
        holds information about the Administrator
    """
    # fields
    first_name = models.CharField(max_length=100, default="", blank=False)
    last_name = models.CharField(max_length=100, default="", blank=False)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=6, choices=gender, blank=False)
    location = models.CharField(max_length=20, blank=False)
    phone_no = models.CharField(max_length=14, default="", blank=False)
    idno = models.BigIntegerField(null=True)
    dob = models.DateField(default=date(2023, 11, 11))
    role = models.CharField(
        max_length=20,  null=True, choices=roles, blank=False
    )
    other_role = models.CharField(
        max_length=20, default="", blank=True
    )

    def __str__(self):
        return self.first_name + self.last_name
    

class ClassRoom(models.Model):
    """
    This is the Classroom Table:
        holds information about a classroom
    """
    name = models.CharField(max_length=100, default="", unique=True)
    grade = models.CharField(max_length=2, choices=grades, null=False, blank=False)
    teacher = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)
    capacity = models.IntegerField(default=0, blank=False)

    def to_json(self):
        data = {}
        data["name"] = self.name
        data["grade"] = self.grade
        data["teacher"] = self.teacher.email
        data["capacity"] = self.capacity

        return data

class Pupil(models.Model):
    """
    This is the Pupils Table:
        holds information about a Pupil
    """
    first_name = models.CharField(max_length=100, default="", blank=True)
    last_name = models.CharField(max_length=100, default="", blank=True)
    birth_certificate_no = models.CharField(max_length=100, blank=False, unique=True)
    class_room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, null=True)
    parent = models.ForeignKey(Users, on_delete=models.CASCADE, blank=False, null=True)
    graduated = models.BooleanField(default=False) # true if pupil has graduated

    def to_json(self):
        data = {}
        data["first_name"] = self.first_name
        data["last_name"] = self.last_name
        data["birth_certificate_no"] = self.birth_certificate_no
        data["class_room"] = self.class_room.name
        data["parent"] = self.parent.email
        data["graduated"] = self.graduated

        return data

class DropOuts(models.Model):
    """
    Will Hold Informations About DropOffs
    """
    pickup_time = models.TimeField(blank=False)
    dropoff_time = models.TimeField(blank=False)
    stage = models.CharField(max_length=100, null=True, blank=False)
