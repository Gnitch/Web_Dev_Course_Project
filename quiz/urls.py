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
    path('quiz_answer_visible/<int:quiz_id>',views.quizAnswerVisible,name='quizAnswerVisible'),
    path('add_question/<int:quiz_id>',views.questionFormSubmit,name='questionFormSubmit'),
    path('view_quiz/<int:quiz_id>',views.quizInfoTeacherView,name='quizInfoTeacherView'),
    path('class_view/<int:class_pk>',views.classView,name='classView'),
    path('post_comment/<int:class_id>',views.postComment,name='postComment'),
    path('delete_comment/<int:comment_id>',views.deleteComment,name='deleteComment'),
    path('quiz_answer/<int:stud_quiz_info_id>/<int:quiz_id>',views.quizAnswer,name='quizAnswer'),    
    path('add_poll/',views.createPoll,name='createPoll'),
    path('add_poll_choices/<int:poll_id>/',views.createPollChoices,name='createPollChoices'),
    path('delete_poll/<int:poll_id>/',views.deletePoll,name='deletePoll'),
    path('activate_poll/<int:poll_id>/',views.activatePoll,name='activatePoll'),
    path('deactivate_poll/<int:poll_id>/',views.deactivatePoll,name='deactivatePoll'),
    path('delete_poll_choices/<int:poll_choice_id>/',views.deletePollChoice,name='deletePollChoice'),
    path('logout/',views.logout,name='logout'),
]

