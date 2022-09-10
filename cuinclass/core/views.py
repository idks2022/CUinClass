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
    
    return HttpResponse(content = answer)

def report(response, id):
    session = Session.objects.get(id=id)
    students = session.student_set.get(id=1)
    return HttpResponse("<h1>%s</h1><br></br><p>%s</p>" %(session.name, str(students.name)))

