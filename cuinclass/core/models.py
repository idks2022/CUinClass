import datetime
from django.db import models

# Create your models here.

class Session(models.Model):
     name = models.CharField(max_length=20)
     
     def __str__(self):
          return self.name


class Student(models.Model):
     session = models.ForeignKey(Session, on_delete=models.CASCADE)
     name = models.CharField(max_length=20)
     signed = models.BooleanField()
     
     def __str__(self):
          return self.name