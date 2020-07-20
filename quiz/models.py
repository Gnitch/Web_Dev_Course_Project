from django.db import models

class Quiz(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    answer = models.TextField(blank=False,null=False)

class Options(models.Model):
    options = models.TextField(blank=True,null=True)
    question = models.ForeignKey(Question,on_delete=models.CASCADE)












