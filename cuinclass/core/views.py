from django.http import HttpResponse
from django.shortcuts import render
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
            cleanName = splitText[0]
            session = Session.objects.get(id=1)

            for student in session.student_set.all():
                if student.name == cleanName:
                    student.signed = True
                    student.save()
                    return HttpResponse(content = answer)
                else: 
                    return HttpResponse(content = None)

        return HttpResponse(content = answer) 

def report(response):
    session = Session.objects.get(id=1)
    # student = session.student_set.get(id=id)
    {"clear":["clear"]}
    if response.POST.get("clear"):
        for student in session.student_set.all():
            student.signed = False
            student.save()
            
    return render(response, 'cuinclass/report.html', {"session":session})

