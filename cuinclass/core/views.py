from django.http import HttpResponse
from django.shortcuts import render
from .forms import *
from django.views.decorators.csrf import csrf_exempt
from core.fr.awsfuncs import find_face
import base64


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

