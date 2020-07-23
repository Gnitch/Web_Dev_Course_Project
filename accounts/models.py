from django.db import models
from django.contrib.auth.models import User

class Job(models.Model):
    choices_status = [
        ('student','Student'),
        ('teacher','Teacher'),
    ]
    status = models.CharField(choices=choices_status,default='student',max_length=10)
    user = models.OneToOneField(User,on_delete=models.CASCADE)

class Class(models.Model):
    class_name = models.CharField(max_length=20)
    user = models.ManyToManyField(User)





