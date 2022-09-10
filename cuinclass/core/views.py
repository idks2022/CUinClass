from django.http import HttpResponse
from django.shortcuts import render
from .forms import *
from django.views.decorators.csrf import csrf_exempt
from core.fr.awsfuncs import find_face
import base64
from .models import Session, Student


def attendance(request):
    return render(request, 'cuinclass/attendance.html')

@csrf_exempt
def fr_image(request):
    if request.method == 'POST':
        base64_image = request.body
        base64_image = base64_image.replace(b'data:image/png;base64,', b'')
        with open("imageToSave.png", "wb") as fh:
            fh.write(base64.decodebytes(base64_image))
        global answer
        answer = find_face('students', "imageToSave.png")
        if(answer):
            responseText = answer
            splitText = responseText.split(".")
            finalText = splitText[0]
            session = Session.objects.get(id=1)
            session.student_set.create(name=str(finalText), signed=True)
    
    return HttpResponse(content = answer)

def report(response):
    session = Session.objects.get(id=1)
    # student = session.student_set.get(id=id)
    return render(response, 'cuinclass/report.html', {"session":session})

