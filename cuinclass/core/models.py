from django.db import models

# Create your models here.

class Student(models.Model):
    # name = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to='uploads/')

def __str__(self):
     return self.title