from django.db import models
import uuid
# Create your models here.
from django.contrib.auth.models import User

class Lecturer(User):
    

    class Meta:
        proxy = True

class AvailableSemester(models.Model):
     myCampId = models.CharField(max_length=20)
     myProgId = models.CharField(max_length=10)
     myAsetId = models.CharField(max_length=10)
     myAsessionId = models.CharField(max_length=10)
     mySemesterId = models.CharField(max_length=1)
     myTheprogType = models.CharField(max_length=10)
     myRemark = models.CharField(max_length=30)



class UploadedScores(models.Model):
     courseGuId  = models.UUIDField( default=uuid.uuid4, editable=True)
     upload_date = models.DateTimeField('upload date')
     scoresheetfile = models.FileField(upload_to='documents/%Y/%m/%d')

