from django.urls import path

from . import views

app_name = 'quiz'
urlpatterns = [
    path('',views.home,name='home'),
    path('add_quiz/',views.addQuiz,name='addQuiz'),
    path('all_student_result/<int:quiz_id>',views.studentQuizResult,name='studentQuizResult'),
    path('delete_quiz/<int:quiz_id>',views.deleteQuiz,name='deleteQuiz'),
    path('delete_answer/<int:question_id>',views.deleteQuestion,name='deleteQuestion'),
    path('view_result/<int:quiz_id>',views.getQuizResult,name='getQuizResult'),
    path('check_answer/<int:question_id>',views.checkAnswer,name='checkAnswer'),
    path('make_quiz_visible/<int:quiz_id>',views.makeQuizVisible,name='makeQuizVisible'),
    path('add_question/<int:quiz_id>',views.questionFormSubmit,name='questionFormSubmit'),
    path('view_quiz/<int:quiz_id>',views.quizInfoTeacherView,name='quizInfoTeacherView'),
    path('class_view/<int:class_pk>',views.classView,name='classView'),
    path('logout/',views.logout,name='logout'),
]

