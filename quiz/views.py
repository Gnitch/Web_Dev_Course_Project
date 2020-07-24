from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as django_logout
from django.http import JsonResponse
from django.template.loader import render_to_string

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

@login_required
def addQuiz(request):

    if request.method == "POST" :
        quiz_form = QuizForm(request.POST)

        if(quiz_form.is_valid()):
            quiz_obj = quiz_form.save()
        return redirect('quiz:quizInfoTeacherView',quiz_id=quiz_obj.id)

    context = {
        'quiz_form':QuizForm(),
        'type':'quiz_form'
    }  
    return render(request, 'quiz/form.html',context)    

def getOptions(question_list):
    option_list = None
    if len(question_list) != 0 :
        question_obj = question_list[0]
        option_list = list(Options.objects.filter(question_id=question_obj.id))
        question_obj.viewed = True
        question_obj = question_obj.save()
        if len(option_list) != 0:
            option_list = option_list[0]
            options = str(option_list.options)
            option_list = []
            option_list = options.split(',')  
    
    return option_list, question_obj

@login_required
def quizInfoTeacherView(request,quiz_id):
    question_obj = None
    option_list = None
    quiz_list = list(Quiz.objects.filter(pk=quiz_id))
    if len(quiz_list) == 0 :
        quiz_obj = None
    else :
        quiz_obj = quiz_list[0] 
        if request.is_ajax():
            question_list = list(Question.objects.filter(quiz_id=quiz_id).filter(viewed=False))                    
            option_list, question_obj = getOptions(question_list)          
            html = render_to_string(
                template_name='quiz/questionForm.html',
                context = {
                    'question_obj':question_obj,
                    'option_list':option_list,
                }
            )    
            data_dict = {"html_from_view": html}
            return JsonResponse(data=data_dict, safe=False)                    
        
        question_list = list(Question.objects.filter(quiz_id=quiz_id))        
        option_list, question_obj = getOptions(question_list)  

    context = {
        'question_obj':question_obj,
        'option_list':option_list,
        'type':'quiz_view',
        'quiz_obj':quiz_obj,
        'question_form':QuestionForm(),
        'options_form':OptionsForm(),        
    }
    return render(request,'quiz/form.html',context)

@login_required
def questionFormSubmit(request,quiz_id):
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        question_form_obj = question_form.save(commit=False)
        question_form_obj.quiz_id = quiz_id
        question_form_obj.save()                   

        if request.POST.get('options') != '' :
            options_form = OptionsForm(request.POST)
            options_form_obj = options_form.save(commit=False)
            options_form_obj.question_id = question_form_obj.id
            options_form_obj.save()            

    return redirect('quiz:quizInfoTeacherView',quiz_id=quiz_id)








