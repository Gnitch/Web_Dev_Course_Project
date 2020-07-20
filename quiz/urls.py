from django.urls import path

from . import views

app_name = 'quiz'
urlpatterns = [
    path('',views.home,name='home'),
    path('form/',views.form,name='form'),
    path('logout/',views.logout,name='logout'),
]


