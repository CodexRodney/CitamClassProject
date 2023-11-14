# Create your models here.
from datetime import date, datetime
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.db import models

gender = (
    ("male", "male"),
    ("female", "female"),
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