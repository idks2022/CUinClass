import datetime
from django.db import models

# Create your models here.

class Session(models.Model):
     name = models.CharField(max_length=20)
     
     def __str__(self):
          return self.name


class Student(models.Model):
     session = models.ForeignKey(Session, on_delete=models.CASCADE)
     id = models.IntegerField(primary_key=True)
     name = models.CharField(max_length=20)
     signed = models.BooleanField(null=True, blank=True)
     updated = models.DateTimeField(auto_now=True, null=True, blank=True)
     image = models.ImageField(upload_to='cuinclass/media/uploads', null=False)
     
     
     def __str__(self):
          return self.name