from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as django_logout
from django.apps import apps
from .models import Quiz, Question, Options
from .forms import QuizForm, QuestionForm, OptionsForm

Job = apps.get_model('accounts','Job')
Class = apps.get_model('accounts','Class')

@login_required
def logout(request):
    if request.user.is_authenticated :
        django_logout(request)
    return redirect('/')

@login_required
def form(request):  
    if request.method == "POST" :
        quiz_form = QuizForm(request.POST)
        question_form = QuestionForm(request.POST)
        options_form = OptionsForm(request.POST)

        if(quiz_form.is_valid() and (question_form.is_valid() and options_form.is_valid())):
            quiz_obj = quiz_form.save()
            question_form_obj = question_form.save(commit=False)
            question_form_obj.quiz_id = quiz_obj.id
            question_form_obj.save()
            options_form_obj = options_form.save(commit=False)
            options_form_obj.question_id = question_form_obj.id
            options_form_obj.save()
        return render(request, 'quiz/form.html')
      
    context = {
        'quiz_form':QuizForm(),
        'question_form':QuestionForm(),
        'options_form':OptionsForm() ,
    }  
    return render(request, 'quiz/form.html',context)

@login_required
def quizList(request):
    quiz_object = Quiz.objects.all()
    question_obj = Question.objects.get(quiz_id=quiz_object[0].id)
    options_obj = Options.objects.get(question_id=question_obj.id)
    options = str(options_obj.options)
    option_list = options.split(',')
    context = {'option_list':option_list,'question_obj':question_obj}
    return render(request,'quiz/quizlist.html',context)

@login_required
def home(request):
    class_list = list(Class.objects.filter(user=request.user))
    context = {
        'class_list':class_list,
    }
    return render(request,'quiz/home.html',context)

@login_required
def classView(request,class_pk):
    class_obj = get_object_or_404(Class,pk=class_pk)
    participant_list = class_obj.user.all()
    teacher_list = []
    student_list = []
    for each_user in participant_list :        
        if each_user.is_superuser :
            pass

        elif str(each_user.job.status)== 'student' :
            student_list.append(each_user)              

        elif str(each_user.job.status)== 'teacher' :
            teacher_list.append(each_user)
        
    context = {
        'class_obj':class_obj,
        'student_list':student_list,
        'teacher_list':teacher_list,
    }
    return render(request,'quiz/class_view.html',context)


