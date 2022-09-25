from django.db import models
import datetime

# Create your models here.
class Student(models.Model):

    name = models.CharField(max_length=100, null=True)
    roll_id = models.CharField(max_length=20, null=True)
    email = models.CharField(max_length=50 ,null=True)

    def __str__(self):

        return self.name


class Interview(models.Model):

    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    start_time = models.DateTimeField(default=datetime.datetime.now())
    end_time = models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):

        return self.student.name

class File(models.Model):
    
    file = models.FileField(upload_to='post_files/', null=True, blank=True)