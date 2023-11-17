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

class Administrator(AbstractUser):
    """
    This is the Administrator table:
        holds information about the Administrator
    """
    # fields
    first_name = models.CharField(max_length=100, default="", blank=True)
    last_name = models.CharField(max_length=100, default="", blank=True)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=6, choices=gender, default="male")
    phone_no = models.CharField(max_length=14, default="", blank=True)
    idno = models.BigIntegerField(null=True)
    dob = models.DateField(default=date(2023, 11, 11))
    role = models.CharField(
        max_length=20, default="admin"
    )

    def __str__(self):
        return self.first_name + self.last_name
    
class Teacher(AbstractBaseUser):
    """
    This is the Teachers table:
        holds information about the Teacher
    """
    # fields
    first_name = models.CharField(max_length=100, default="", blank=True)
    last_name = models.CharField(max_length=100, default="", blank=True)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=6, choices=gender, default="male")
    phone_no = models.CharField(max_length=14, default="", blank=True)
    idno = models.BigIntegerField(null=True)
    dob = models.DateField(default=date(2023, 11, 11))
    role = models.CharField(
        max_length=20, default="teacher"
    )

    def __str__(self):
        return self.first_name + self.last_name

class Parent(AbstractBaseUser):
    """
    This is the Parent table:
        holds information about the Parent
    """
    # fields
    first_name = models.CharField(max_length=100, default="", blank=True)
    last_name = models.CharField(max_length=100, default="", blank=True)
    location = models.CharField(max_length=100, default="", blank=True)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=6, choices=gender, default="male")
    phone_no = models.CharField(max_length=14, default="", blank=True)
    idno = models.BigIntegerField(null=True)
    dob = models.DateField(default=date(2023, 11, 11))
    role = models.CharField(
        max_length=20, default="parent"
    )

    def __str__(self):
        return self.first_name + self.last_name

class Driver(AbstractBaseUser):
    """
    This is the Driver table:
        holds information about the Driver
    """
    # fields
    first_name = models.CharField(max_length=100, default="", blank=True)
    last_name = models.CharField(max_length=100, default="", blank=True)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=6, choices=gender, default="male")
    phone_no = models.CharField(max_length=14, default="", blank=True)
    idno = models.BigIntegerField(null=True)
    dob = models.DateField(default=date(2023, 11, 11))
    role = models.CharField(
        max_length=20, default="driver"
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
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
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
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, blank=False, null=True)
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


