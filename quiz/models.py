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

class Quiz(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    classes = models.ManyToManyField(Class)
    make_visible = models.BooleanField(default=False)
    total_questions = models.IntegerField(primary_key=False,default=0)

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.TextField(blank=False,null=False)
    answer = models.TextField(blank=False,null=False)
    multiple_answer = models.BooleanField(default=False,primary_key=False)
    figure = models.ImageField(upload_to='quiz/figures',null=True, blank=True)

class Options(models.Model):
    options = models.TextField(blank=True,null=True)
    question = models.ForeignKey(Question,on_delete=models.CASCADE)

class StudentQuizInfo(models.Model):
    completed = models.BooleanField(primary_key=False,default=False)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField(primary_key=False,default=0)
    quiz_questions = models.ManyToManyField(Question)
    user = models.ForeignKey(User,on_delete=models.CASCADE)



