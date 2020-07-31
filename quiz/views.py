from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.template.loader import render_to_string
import os

import Quiz_system.settings as settings
from .models import Quiz, Question, Options, StudentQuizInfo, Job, Class, Comments
from .forms import QuizForm, QuestionForm, OptionsForm, CommentsForm


@login_required
def logout(request):
    if request.user.is_authenticated:
        django_logout(request)
    return redirect('/')


@login_required
def home(request):
    class_list = list(Class.objects.filter(user=request.user))
    faculty_count = []
    student_count = []
    quiz_count = []
    for each in class_list:
        temp_teach = []
        temp_stud = []
        for user in each.user.all():
            if str(user.job.status) == 'teacher':
                temp_teach.append(user)
            else:
                temp_stud.append(user)

        faculty_count.append(len(temp_teach))
        student_count.append(len(temp_stud))
        temp_teach.clear()
        temp_stud.clear()
        quiz_count.append(Quiz.objects.filter(
            make_visible=True).filter(classes=each).count())

    class_info = zip(class_list, faculty_count, student_count, quiz_count)
    context = {
        'class_list': class_info
    }
    return render(request, 'quiz/home.html', context)


@login_required
def classView(request,class_pk):
    stud_info = []
    quiz_info = []
    class_obj = get_object_or_404(Class,pk=class_pk)
    if str(request.user.job.status) == 'student':
        quiz_list = list(Quiz.objects.filter(make_visible=True).filter(classes=class_obj))            
        student_quiz_info = []
        if len(quiz_list) != 0:
            for quiz in quiz_list :
                stud_info = list(StudentQuizInfo.objects.filter(quiz_id=quiz.id).filter(user_id=request.user.id))            
                if len(stud_info) != 0 :
                    student_quiz_info.append(stud_info[0])  
                else :
                    student_quiz_info.append(None)

        quiz_info = zip(quiz_list,student_quiz_info)      
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

    user_list = []
    if Comments.objects.filter(clas_id=class_pk).exists():
        comments = get_list_or_404(Comments,clas_id=class_pk)
        for comment in comments :            
            user_list.append(get_object_or_404(User,pk=comment.user_id))
        
    else :
        comments = []

    user_comments_list = zip(user_list,comments)
    context = {
        'quiz_info':quiz_info,
        'class_obj':class_obj,
        'student_list':student_list,
        'teacher_list':teacher_list,
        'quiz_list':quiz_list,
        'comments_form':CommentsForm(),   
        'user_comments_list':user_comments_list,       
    }
    return render(request,'quiz/class_view.html',context)


@login_required
def addQuiz(request):

    if request.method == "POST":
        quiz_form = QuizForm(request.POST)
        classList = request.POST.getlist('classList')
        if(quiz_form.is_valid()):
            quiz_obj = quiz_form.save()
            for each_class in classList:
                quiz_obj.classes.add(Class.objects.get(pk=int(each_class)))
            quiz_obj.save()

            return redirect('quiz:quizInfoTeacherView', quiz_id=quiz_obj.id)

    class_list = get_list_or_404(Class, user=request.user)
    context = {
        'quiz_form': QuizForm(),
        'type': 'quiz_form',
        'class_list': class_list,
    }
    return render(request, 'quiz/form.html', context)


@login_required
def makeQuizVisible(request, quiz_id):
    if request.user.job.status == 'teacher':
        quiz_obj = get_object_or_404(Quiz, pk=quiz_id)
        quiz_obj.make_visible = True
        question_list = get_list_or_404(Question, quiz_id=quiz_id)
        quiz_obj.total_questions = len(question_list)
        quiz_obj.save()

    return redirect('quiz:quizInfoTeacherView', quiz_id=quiz_id)


@login_required
def quizAnswerVisible(request, quiz_id):
    if request.user.job.status == 'teacher':
        print("YEss")
        quiz_obj = get_object_or_404(Quiz, pk=quiz_id)
        quiz_obj.answer_available = True
        quiz_obj.save()

    return redirect('quiz:quizInfoTeacherView', quiz_id=quiz_id)


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
def quizInfoTeacherView(request, quiz_id):
    student_list = []
    random_question_obj = None
    teacher_question_list = None
    option_list = []
    if str(request.user.job.status) == 'student':
        quiz_list = list(Quiz.objects.filter(
            make_visible=True).filter(pk=quiz_id))
    else:
        quiz_list = list(Quiz.objects.filter(pk=quiz_id))

    if len(quiz_list) == 0:
        quiz_obj = None
    else:
        quiz_obj = quiz_list[0]
        random_question_obj = None
        if str(request.user.job.status) == 'student':
            if not StudentQuizInfo.objects.filter(quiz_id=quiz_id).filter(user_id=request.user.id).exists():
                student_quiz_info = StudentQuizInfo.objects.create(
                    quiz_id=quiz_id,
                    user_id=request.user.id
                )
                question_list = list(Question.objects.filter(quiz_id=quiz_id))
                for question in question_list:
                    student_quiz_info.quiz_questions.add(question)
                student_quiz_info.save()
            question_obj_list = list(StudentQuizInfo.objects.filter(
                quiz_id=quiz_id).filter(user_id=request.user.id))
            if len(question_obj_list) != 0:
                if quiz_obj.answer_available == True:
                    return redirect('quiz:quizAnswer', stud_quiz_info_id=question_obj_list[0].id, quiz_id=quiz_id)

                if question_obj_list[0].quiz_questions.exists():
                    random_question_obj = question_obj_list[0].quiz_questions.order_by(
                        '?').first()
                    option_list = getOptions(random_question_obj)

                else:
                    return redirect('quiz:getQuizResult', quiz_id=quiz_id)

        else:
            question_obj_list = list(Question.objects.filter(quiz_id=quiz_id))
            for question in question_obj_list:
                option_list.append(
                    list(Options.objects.filter(question_id=question.id)))

            quiz_obj = get_object_or_404(Quiz, pk=quiz_id)
            student_list = list(
                StudentQuizInfo.objects.filter(quiz_id=quiz_id))
            user_list = []
            for student in student_list:
                user_list.append(get_object_or_404(User, pk=student.user_id))

            student_list = zip(user_list, student_list)
            teacher_question_list = zip(question_obj_list, option_list)

    context = {
        'student_list': student_list,
        'question_obj': random_question_obj,
        'option_list': option_list,
        'type': 'quiz_view',
        'action': 'check',
        'quiz_obj': quiz_obj,
        'teacher_question_list': teacher_question_list,
        'question_form': QuestionForm(),
        'options_form': OptionsForm(),
    }
    return render(request, 'quiz/form.html', context)


def ansCheck(request, question_id):
    result = ''
    user_ans = ''
    random_question_obj = get_object_or_404(Question, pk=question_id)
    student_quiz_info = list(StudentQuizInfo.objects.filter(
        quiz_id=random_question_obj.quiz_id).filter(user_id=request.user.id))
    student_quiz_info = student_quiz_info[0]
    user_ans = request.GET.get('checked_array')
    input_answer = request.GET.get('inputText')

    answer_list = []
    if input_answer is not None:
        if input_answer == str(random_question_obj.answer):
            result = 'correct'
            scoreSave(student_quiz_info)

        else:
            result = 'incorrect'
    elif user_ans is not None:
        user_ans = user_ans[:-1]
        user_answers = user_ans.split(',')

        if ',' in random_question_obj.answer:
            answer_list = str(random_question_obj.answer).split(',')
        else:
            answer_list.append(random_question_obj.answer)

        flag = True
        for answer in user_answers:
            if answer not in answer_list:
                flag = False
                break
        if flag == True:
            result = 'correct'
            scoreSave(student_quiz_info)

        else:
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
    student_quiz_info.completed = True
    student_quiz_info.save()
    quiz_obj = get_object_or_404(Quiz,pk=quiz_id)
    context = {'student_quiz_info':student_quiz_info,'quiz_obj':quiz_obj}
    return render(request, 'quiz/quizResult.html',context)

@login_required
def questionFormSubmit(request, quiz_id):
    if request.method == 'POST':
        question_form = QuestionForm(request.POST, request.FILES)
        question_form_obj = question_form.save(commit=False)
        question_form_obj.quiz_id = quiz_id
        question_form_obj.save()

        if request.POST.get('options') != '':
            options_form = OptionsForm(request.POST)
            options_form_obj = options_form.save(commit=False)
            options_form_obj.question_id = question_form_obj.id
            options_form_obj.save()

    return redirect('quiz:quizInfoTeacherView', quiz_id=quiz_id)


@login_required
def checkAnswer(request, question_id):
    if request.is_ajax():
        print("AJAX")
        random_question_obj = None
        option_list = None
        result = ansCheck(request, question_id)
        question_obj = get_object_or_404(Question, pk=question_id)
        quiz = get_object_or_404(Quiz, pk=question_obj.quiz_id)
        print(quiz.title)
        question_obj_list = list(StudentQuizInfo.objects.filter(quiz_id=question_obj.quiz_id).filter(user_id=request.user.id))
        print(question_obj_list[0].id)
        if len(question_obj_list) != 0 :
            question_obj_list[0].quiz_questions.remove(question_obj)
            print(question_obj_list[0].quiz_questions.all())
            if question_obj_list[0].quiz_questions.exists():
                random_question_obj = question_obj_list[0].quiz_questions.order_by(
                    '?').first()
                option_list = getOptions(random_question_obj)
                ques_id = random_question_obj.id
                html = render_to_string(
                    template_name='quiz/questionForm.html',
                    context={
                        'quiz_obj': quiz,
                        'question_obj': random_question_obj,
                        'option_list': option_list,
                    }
                )
                data_dict = {"html_from_view": html,
                             'result': result, 'id': ques_id}

            else:
                print("Quiz Over")
                html = render_to_string(
                    template_name='quiz/questionForm.html',
                    context={
                        'question_obj': None,
                        'option_list': None,
                    }
                )
                data_dict = {"html_from_view": html,
                             'result': result, 'quiz_id': question_obj.quiz_id}

            return JsonResponse(data=data_dict, safe=False)

    else:
        redirect('/quiz/')


@login_required
def studentQuizResult(request, quiz_id):
    quiz_obj = get_object_or_404(Quiz, pk=quiz_id)
    student_list = list(StudentQuizInfo.objects.filter(quiz_id=quiz_id))
    user_list = []
    for student in student_list:
        user_list.append(get_object_or_404(User, pk=student.user_id))

    student_list = zip(user_list, student_list)
    context = {'quiz_obj': quiz_obj, 'student_list': student_list}
    return render(request, 'quiz/StudentQuizResult.html', context)


@login_required
def deleteQuestion(request, question_id):
    question_obj = get_object_or_404(Question, pk=question_id)
    quiz_obj = get_object_or_404(Quiz, pk=question_obj.quiz_id)
    if quiz_obj.make_visible == False and str(request.user.job.status) == 'teacher':
        Options.objects.filter(question_id=question_id).delete()
        if question_obj.figure is not None:
            os.remove(os.path.join(settings.MEDIA_ROOT,
                                   str(question_obj.figure.name)))

        question_obj.delete()

    return redirect('quiz:quizInfoTeacherView', quiz_id=question_obj.quiz_id)


@login_required
def deleteQuiz(request, quiz_id):
    quiz_obj = get_object_or_404(Quiz, pk=quiz_id)
    question_list = get_list_or_404(Question, quiz_id=quiz_id)
    if quiz_obj.make_visible == False and str(request.user.job.status) == 'teacher':
        for question in question_list:
            Options.objects.filter(question_id=question.id).delete()
            if question.figure is not None:
                os.remove(os.path.join(settings.MEDIA_ROOT,
                                       str(question.figure.name)))

            question.delete()
        quiz_obj.delete()

    return redirect('/quiz/')


@login_required
def postComment(request, class_id):
    if request.method == 'POST':
        form = CommentsForm(request.POST)
        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.user_id = request.user.id
            form_obj.clas_id = class_id
            form_obj.save()

    return redirect('quiz:classView', class_pk=class_id)


@login_required
def deleteComment(request, comment_id):
    comment_obj = get_object_or_404(Comments,pk=comment_id)
    class_obj = get_object_or_404(Class,pk=comment_obj.clas_id)
    comment_obj.delete()
    return redirect('quiz:classView',class_pk=class_obj.id)

@login_required
def quizAnswer(request,stud_quiz_info_id,quiz_id):
    quiz_obj = get_object_or_404(Quiz,pk=quiz_id)
    if quiz_obj.answer_available == True :
        stud_quiz_info_obj = get_object_or_404(StudentQuizInfo,pk=stud_quiz_info_id)
        quesion_list = get_list_or_404(Question,quiz_id=quiz_id)
        context = {'quiz_obj':quiz_obj,'stud_quiz_info_obj':stud_quiz_info_obj,'quesion_list':quesion_list}
        return render(request, 'quiz/quizAnswer.html',context)        

    else :
        return redirect('quiz:quizInfoTeacherView',quiz_id=quiz_id)

@login_required
def deleteComment(request, comment_id):
    comment_obj = get_object_or_404(Comments, pk=comment_id)
    class_obj = get_object_or_404(Class, pk=comment_obj.clas_id)
    comment_obj.delete()
    return redirect('quiz:classView', class_pk=class_obj.id)


@login_required
def quizAnswer(request, stud_quiz_info_id, quiz_id):
    quiz_obj = get_object_or_404(Quiz, pk=quiz_id)
    if quiz_obj.answer_available == True:
        stud_quiz_info_obj = get_object_or_404(
            StudentQuizInfo, pk=stud_quiz_info_id)
        quesion_list = get_list_or_404(Question, quiz_id=quiz_id)
        context = {'quiz_obj': quiz_obj,
                   'stud_quiz_info_obj': stud_quiz_info_obj, 'quesion_list': quesion_list}
        return render(request, 'quiz/quizAnswer.html', context)

    else:
        return redirect('quiz:quizInfoTeacherView', quiz_id=quiz_id)
