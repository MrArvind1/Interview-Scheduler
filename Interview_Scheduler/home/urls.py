from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('fetch/data/student/', views.fetchLatestStudentData, name="fetchLatestStudentData"),
    path('schedule/interview/', views.scheduleInterview, name="scheduleInterview"),
    path('get/data/interview/', views.getInterviewData, name="getInterviewData"),
    path('edit/interview/', views.editInterview, name="editInterview"),
    path('delete/interview/<str:interview_id>', views.deleteInterview, name="deleteInterview"),


]
