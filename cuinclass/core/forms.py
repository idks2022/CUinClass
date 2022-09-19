from dataclasses import fields
from .models import *
from django.forms import ModelForm
from django import forms
  
class UploadForm(ModelForm):
    session = forms.TextInput()
    id = forms.TextInput()
    name = forms.TextInput()
    image = forms.ImageField()
    class Meta:
        model = Student
        fields = ['session', 'id', 'name', 'image',]
        help_texts = {'session':"Class to appand",'id':"Personal ID", 'name':"Firstname Lastname",}