from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from core.fr.awsfuncs import find_face, add_faces_to_collection
import base64
from .forms import UploadForm
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

def add(request):
    if request.POST:
        form = UploadForm(request.POST, request.FILES)
        print(request.FILES)
        if form.is_valid():
            form.save()
            #uploading the saved image to s3 collection for 'rekognition'
            student = Student.objects.get(id=request.POST['id'])
            studentNameRaw = student.name
            studentNameSplit = studentNameRaw.split(" ")
            studentNameToCollection = studentNameSplit[0]+"_"+studentNameSplit[1] #correct image name format
            print(studentNameToCollection+" saved to database") 
            studentImagePath = student.image
            studentImagePathSplit = str(studentImagePath).split("/")
            studentImageName = studentImagePathSplit[3] #correct image path format
            print(studentImageName)
            global uploadToS3
            try:
                uploadToS3 = add_faces_to_collection('custudents',studentImageName,studentNameToCollection,'students')
                print("face image uploaded to collection successfully")
            except Exception as e:
                print("face image upload to collection failed!")
                student.delete()
                print("object removed from database")
            #done uploading face to collection
            
        
        return redirect(add)
    return render(request, 'cuinclass/add.html', {'form' : UploadForm})