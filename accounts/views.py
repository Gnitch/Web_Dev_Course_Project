import secrets
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail

from .forms import UserAuthenticationForm
from django.contrib.auth import authenticate, login

def userLogin(request):
    if request.method == 'POST' :
        form =  UserAuthenticationForm(request=request,data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None :
                login(request, user)
                return redirect('/quiz/')

            else :
                form =  UserAuthenticationForm()
                message = 'Authentication Error'
                type_form = 'signup'
                context = {'form':form,'message':message,'type_form':type_form}
                return render(request,'accounts/authentication.html',context)    

        else :
            form =  UserAuthenticationForm()
            message = 'Invalid Credentials'
            type_form = 'login'
            context = {'form':form,'message':message,'type_form':type_form}
            return render(request,'accounts/authentication.html',context)   

    else :
        form =  UserAuthenticationForm()
        message = ''
        type_form = 'login'
        context = {'form':form,'message':message,'type_form':type_form}
        return render(request,'accounts/authentication.html',context)  

