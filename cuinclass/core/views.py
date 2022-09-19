from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
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
            session = Session.objects.get(id=1)
            for student in session.student_set.all():
                if str(student.id) == str(answer):
                    student.signed = True
                    student.save()
                    return HttpResponse(content = str(student.name))
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
            print("form saved")
            #uploading the saved image to s3 collection for 'rekognition'
            student = Student.objects.get(id=request.POST['id'])
            studentID = str(student.id)
            print("external Image ID = student ID = "+studentID)
            # studentNameRaw = student.name
            # studentNameSplit = studentNameRaw.split(" ")
            # studentNameToCollection = studentNameSplit[0]+"_"+studentNameSplit[1] #correct image name format (First_Last)
            print(studentID+" saved to database") 
            studentImage = str(student.image)
            print(studentImage)
            global uploadToS3
            try:
                uploadToS3 = add_faces_to_collection('custudents',studentImage,studentID,'students')
                if(uploadToS3):
                    print("face image uploaded to collection successfully")
                    messages.success(request, 'Student has been successfully added to database')
                else: 
                    student.delete()
                    print("Face was not detected, object removed from database.")
                    messages.error(request, 'Face was not detected, student was not added to database.')
            except Exception as e:
                print("face image upload to collection failed!")
                student.delete()
                print("object removed from database")
                messages.error(request, 'Error submitting the form, if error recurrent check with the IT.')
            # done uploading face to collection
            
        # return redirect(add)
    return render(request, 'cuinclass/add.html', {'form' : UploadForm})