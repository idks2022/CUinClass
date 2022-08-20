from django.shortcuts import render
from django.http import HttpResponse


def attendance(request):

    return render(request,'cuinclass/attendance.html')