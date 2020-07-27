from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as django_logout
from django.http import JsonResponse
from django.template.loader import render_to_string

from django.apps import apps
from .models import Quiz, Question, Options, StudentQuizInfo, Job, Class
from .forms import QuizForm, QuestionForm, OptionsForm

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
    if str(request.user.job.status) == 'student':
        quiz_list = list(Quiz.objects.filter(make_visible=True).filter(classes=class_obj))            
    else :
        quiz_list = list(Quiz.objects.filter(classes=class_obj))            

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
        'quiz_list':quiz_list
    }
    return render(request,'quiz/class_view.html',context)

@login_required
def addQuiz(request):

    if request.method == "POST" :
        quiz_form = QuizForm(request.POST)
        classList = request.POST.getlist('classList')        
        if(quiz_form.is_valid()):
            quiz_obj = quiz_form.save()
            for each_class in classList :
                quiz_obj.classes.add(Class.objects.get(pk=int(each_class)))
            quiz_obj.save()

        return redirect('quiz:quizInfoTeacherView',quiz_id=quiz_obj.id)

    class_list = get_list_or_404(Class,user=request.user)
    context = {
        'quiz_form':QuizForm(),
        'type':'quiz_form',
        'class_list':class_list,
    }  
    return render(request, 'quiz/form.html',context)    

@login_required
def makeQuizVisible(request, quiz_id):
    if request.user.job.status == 'teacher' :
        quiz_obj = get_object_or_404(Quiz,pk=quiz_id)
        quiz_obj.make_visible = True
        question_list = get_list_or_404(Question,quiz_id=quiz_id)
        quiz_obj.total_questions = len(question_list)
        quiz_obj.save()        
    
    return redirect('quiz:quizInfoTeacherView',quiz_id=quiz_id)

def getOptions(question_obj):
    option_list = None
    option_list = list(Options.objects.filter(question_id=question_obj.id))
    if len(option_list) != 0:
        option_list = option_list[0]
        options = str(option_list.options)
        option_list = []
        option_list = options.split(',')  
    return option_list

@login_required
def quizInfoTeacherView(request,quiz_id):
    random_question_obj = None
    teacher_question_list = None
    option_list = []
    if str(request.user.job.status) == 'student':
        quiz_list = list(Quiz.objects.filter(make_visible=True).filter(pk=quiz_id))
    else :
        quiz_list = list(Quiz.objects.filter(pk=quiz_id))
    
    if len(quiz_list) == 0 :
        quiz_obj = None
    else :
        quiz_obj = quiz_list[0] 
        random_question_obj = None
        if str(request.user.job.status) == 'student':
            if not StudentQuizInfo.objects.filter(user_id=request.user.id).exists() :
                student_quiz_info = StudentQuizInfo.objects.create(
                    quiz_id = quiz_id,
                    user_id = request.user.id
                ) 
                question_list = list(Question.objects.filter(quiz_id=quiz_id))                
                for question in question_list :
                    student_quiz_info.quiz_questions.add(question)
                student_quiz_info.save()
            question_obj_list = list(StudentQuizInfo.objects.filter(quiz_id=quiz_id).filter(user_id=request.user.id))

            if len(question_obj_list) != 0 :
                if question_obj_list[0].quiz_questions.exists() :  
                    random_question_obj = question_obj_list[0].quiz_questions.order_by('?').first()
                    option_list = getOptions(random_question_obj)                    

                else :
                    return redirect('quiz:getQuizResult',quiz_id=quiz_id)

        else :                  
            question_obj_list = list(Question.objects.filter(quiz_id=quiz_id))                        
            for question in question_obj_list :
                option_list.append(list(Options.objects.filter(question_id=question.id)))

            teacher_question_list = zip(question_obj_list,option_list)                  
        
    context = {
        'question_obj':random_question_obj,
        'option_list':option_list,
        'type':'quiz_view',
        'action':'check',
        'quiz_obj':quiz_obj,
        'teacher_question_list':teacher_question_list,
        'question_form':QuestionForm(),
        'options_form':OptionsForm(),        
    }
    return render(request,'quiz/form.html',context)

def ansCheck(request, question_id):
    result = ''
    user_ans = ''    
    random_question_obj = get_object_or_404(Question,pk=question_id)  
    student_quiz_info = list(StudentQuizInfo.objects.filter(quiz_id=random_question_obj.quiz_id).filter(user_id=request.user.id))
    student_quiz_info = student_quiz_info[0]    
    user_ans = request.GET.get('checked_array')          
    input_answer = request.GET.get('inputText') 
      
    answer_list = []        
    print(input_answer,user_ans)
    if input_answer is not None :
        if input_answer == str(random_question_obj.answer) :
            result = 'correct'
            scoreSave(student_quiz_info)


        else :
            result = 'incorrect'
    elif user_ans is not None :               
        user_ans = user_ans[:-1]
        user_answers = user_ans.split(',')          
        
        if ',' in random_question_obj.answer :
            answer_list = str(random_question_obj.answer).split(',')
        else :
            answer_list.append(random_question_obj.answer)

        flag = True
        for answer in user_answers :
            if answer not in answer_list :
                flag = False
                break
        if flag == True :
            result = 'correct' 
            scoreSave(student_quiz_info)

        else :
            result = 'incorrect'
    return result

def scoreSave(student_quiz_info):
    score = student_quiz_info.score
    score += 1                                       
    student_quiz_info.score = score
    student_quiz_info.save()  

@login_required
def getQuizResult(request, quiz_id):
    student_quiz_info = list(StudentQuizInfo.objects.filter(quiz_id=quiz_id).filter(user_id=request.user.id))[0]
    quiz_obj = get_object_or_404(Quiz,pk=quiz_id)
    context = {'student_quiz_info':student_quiz_info,'quiz_obj':quiz_obj}
    return render(request, 'quiz/quizResult.html',context)

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

  

@login_required
def checkAnswer(request, question_id):
    if request.is_ajax():      
        print("AJAX")
        random_question_obj = None
        option_list = None
        result = ansCheck(request,question_id)
        question_obj = get_object_or_404(Question,pk=question_id)        
        question_obj_list = list(StudentQuizInfo.objects.filter(quiz_id=question_obj.quiz_id).filter(user_id=request.user.id))

        if len(question_obj_list) != 0 :
            question_obj_list[0].quiz_questions.remove(question_obj)
            print(question_obj_list[0].quiz_questions.all())            
            if question_obj_list[0].quiz_questions.exists() :  
                random_question_obj = question_obj_list[0].quiz_questions.order_by('?').first()
                option_list = getOptions(random_question_obj) 
                ques_id = random_question_obj.id
                html = render_to_string(
                    template_name='quiz/questionForm.html',
                    context = {
                        'question_obj':random_question_obj,
                        'option_list':option_list,
                    }
                ) 
                data_dict = {"html_from_view": html,'result':result,'id':ques_id}
          
            else :
                print("Quiz Over")    
                html = render_to_string(
                    template_name='quiz/questionForm.html',
                    context = {
                        'question_obj':None,
                        'option_list':None,
                    }
                )                             
                data_dict = {"html_from_view": html,'result':result,'quiz_id':question_obj.quiz_id}
            
            return JsonResponse(data=data_dict, safe=False) 

    else :
        redirect('/quiz/')



















