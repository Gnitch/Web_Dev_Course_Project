from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Job(models.Model):
    choices_status = [
        ('student','Student'),
        ('teacher','Teacher'),
    ]
    status = models.CharField(choices=choices_status,default='student',max_length=10)
    user = models.OneToOneField(User,on_delete=models.CASCADE)

class Class(models.Model):
    class_name = models.CharField(max_length=20)
    year = models.IntegerField(primary_key=False,null=False,blank=False)
    branch = models.CharField(max_length=50)
    user = models.ManyToManyField(User)

class Quiz(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    classes = models.ManyToManyField(Class)
    make_visible = models.BooleanField(default=False)
    total_questions = models.IntegerField(primary_key=False,default=0)
    answer_available = models.BooleanField(primary_key=False,default=False)
    timer = models.IntegerField(primary_key=False,null=True,blank=True,validators=[MinValueValidator(9), MaxValueValidator(31)],)

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.TextField(blank=False,null=False)
    answer = models.TextField(blank=False,null=False)
    multiple_answer = models.BooleanField(default=False,primary_key=False)
    figure = models.ImageField(upload_to='quiz/figures',null=True, blank=True)   
    explanation = models.TextField(null=True,blank=True) 

class Options(models.Model):
    options = models.TextField(blank=True,null=True)
    question = models.ForeignKey(Question,on_delete=models.CASCADE)

class StudentQuizInfo(models.Model):
    completed = models.BooleanField(primary_key=False,default=False)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField(primary_key=False,default=0)
    quiz_questions = models.ManyToManyField(Question)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

class Comments(models.Model):
    comment = models.TextField(blank=False,null=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    spam = models.BooleanField(null=True,blank=True,primary_key=False)
    clas = models.ForeignKey(Class,on_delete=models.CASCADE)


class Poll(models.Model):
    title = models.CharField(max_length=250)
    classes = models.ManyToManyField(Class)
    activate = models.BooleanField(default=False,primary_key=False)

class PollChoices(models.Model):
    choice = models.TextField(blank=False,null=False)
    poll = models.ForeignKey(Poll,on_delete=models.CASCADE)
    user = models.ManyToManyField(User)




