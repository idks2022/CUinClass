from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import *
from django.conf import settings
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from core.fr.awsfuncs import find_face
import json
import pyautogui
import base64
from datauri import DataURI


def attendance(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
  
        if form.is_valid():
            form.save()
            return redirect('attendance')
    else:
        form = StudentForm()
    return render(request, 'cuinclass/attendance.html', {'form' : form})

@csrf_exempt
def fr_image(request):
    if request.method == 'POST':
        base64_image = request.body
        base64_image = base64_image.replace(b'data:image/png;base64,', b'')
        with open("imageToSave.png", "wb") as fh:
            fh.write(base64.decodebytes(base64_image))
        find_face('students', "imageToSave.png")
        
    return HttpResponse(content="Got the image")