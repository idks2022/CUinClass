from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import *
from django.conf import settings
from django.contrib import messages
import pyautogui

def attendance(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
  
        if form.is_valid():
            form.save()
            return redirect('attendance')
    else:
        form = StudentForm()
    return render(request, 'cuinclass/attendance.html', {'form' : form})
