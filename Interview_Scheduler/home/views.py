from django.shortcuts import render, HttpResponse
from .models import *
import pandas as pd
from io import BytesIO
from django.contrib.staticfiles.views import serve
from django.conf import settings
from datetime import datetime
from django.http.response import JsonResponse
from django.core import serializers

# Create your views here.
def home(request):

    interviews = Interview.objects.all()

    return render(request, "home/home.html", context={"interviews": interviews})

def fetchLatestStudentData(request):

    data = Student.objects.all()

    df = pd.DataFrame(index=range(0,len(data)), columns=["Email"])

    for i in range(len(data)):
        df["Email"][i] = data[i].email

    file_path = 'static/students.xlsx'

    datatoexcel = pd.ExcelWriter(file_path)

    df.to_excel(datatoexcel)

    datatoexcel.save()

    return HttpResponse("Student data updated successfully.")

def scheduleInterview(request):

    file = request.FILES.get("file")
    start_time = request.POST.get("start_time")
    end_time = request.POST.get("end_time")

    if str(file).endswith('.csv'):
        # csv file
        data=pd.read_csv(file)
    elif str(file).endswith('.xlsx'):
        # excel file
        data=pd.read_excel(file)

    message = schedule(data, start_time, end_time)

    return JsonResponse({"message": message}, status=200)

def schedule(data, start_time, end_time):

    start_time = datetime.strptime(start_time, "%Y-%m-%dT%H:%M")
    end_time = datetime.strptime(end_time, "%Y-%m-%dT%H:%M")

    error = ""

    interviews_scheduled = 0

    interview_schedule_list = []

    for email in data["Email"]:

        try:
            student = Student.objects.get(email=email)
        except:
            error += "Student with " + email + " was not found in the database.\n"

        interviews = Interview.objects.filter(student=student)

        isClashFound = foundInterviewClash(interviews, start_time, end_time)

        if not isClashFound:
            interviews_scheduled += 1

            interview_schedule_list.append(student)

        else:
            error += "Student with " + email + " has another interview scheduled in the given timing.\n"

    if interviews_scheduled >= 2:

        for student in interview_schedule_list:

            Interview.objects.create(student=student,
                                    start_time=start_time,
                                    end_time=end_time)

            error += "Interview Scheduled for student with " + student.email + ".\n"
            
    else:
        error = "Interview is scheduled none of the students.\n" + error

    return error

def foundInterviewClash(interviews, start_time, end_time, ignoreID = 0):

    for interview in interviews:

        if interview.id == ignoreID:
            continue
        
        if str(end_time) < str(interview.start_time):
            continue
        
        if str(start_time) > str(interview.end_time):
            continue
        
        return True

    return False

def getInterviewData(request):

    interview_id = int(request.GET.get("interview_id"))
    interview = Interview.objects.get(id = interview_id)

    return JsonResponse({"data": serializers.serialize('json', [interview])}, status=200)

def editInterview(request):

    start_time = request.POST.get("start_time")
    end_time = request.POST.get("end_time")
    interview_id = int(request.POST.get("interview_id"))

    student = Interview.objects.get(id = interview_id).student

    interviews = Interview.objects.filter(student = student)

    isClashFound = foundInterviewClash(interviews, start_time, end_time, ignoreID = interview_id)

    if not isClashFound:
        interview = Interview.objects.get(id = interview_id)
        interview.start_time = datetime.strptime(start_time, "%Y-%m-%dT%H:%M")
        interview.end_time = datetime.strptime(end_time, "%Y-%m-%dT%H:%M")
        interview.save()
        message = "Timings updated successfully."

    else:
        message = "Student has another interview scheduled in the given timing."

    return JsonResponse({"message": message}, status=200)

def deleteInterview(request, interview_id):

    Interview.objects.get(id = int(interview_id)).delete()

    return HttpResponse("Interview Record Deleted.")