from django.shortcuts import render, redirect, get_list_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test
from django.apps import apps

from .forms import UserAuthenticationForm, UserSignUpForm


Job = apps.get_model('quiz','Job')
Class = apps.get_model('quiz','Class')

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

@user_passes_test(lambda u : u.is_superuser)
def add_classes(request):
    if request.method == 'POST' :
        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'THIS IS NOT A CSV FILE')

            io_string = io.StringIO(data_set)
            next(io_string)
            for column in csv.reader(io_string, delimiter=',', quotechar="|"):
                _, created = Profile.objects.update_or_create(
                    class_name=column[0],
                    year=column[1],
                    branch=column[2],
                )
        
        return render(request,'accounts/authentication.html',context)  

@user_passes_test(lambda u : u.is_superuser)
def userRegister(request):
    if request.method == 'POST' :
        job = request.POST.get('job')
        form =  UserSignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            email = form.cleaned_data.get('email')

            if(password1 == password2):
                if User.objects.filter(username=username).exists():
                    form =  UserSignUpForm(request.GET)                
                    message = 'Username already exist'
                    type_form = 'signup'
                    context = {'form':form,'message':message,'type_form':type_form}
                    return render(request,'accounts/admin_stuff.html',context)
        
                elif User.objects.filter(email=email).exists():
                    form =  UserSignUpForm(request.GET)
                    message = 'Email already exist'
                    type_form = 'signup'
                    context = {'form':form,'message':message,'type_form':type_form}
                    return render(request,'accounts/admin_stuff.html',context)

                else :
                    user = User.objects.create_user(username=username,password=password1,email=email)
                    user_obj = user.save()
                    
                    
                    if job == 'teacher' :
                        job_obj = Job.objects.create(
                            status = 'teacher',                            
                        )
                        job_obj.user.add(user)
                        job_obj.save()
                    else :
                        teach_obj = Job.objects.create(
                            status = 'teacher',                            
                        )
                        job_obj.user.add(user)
                        job_obj.save()

                    return redirect('/')
                    

            else :
                form =  UserSignUpForm(request.GET)
                message = 'Passwords do not match'
                type_form = 'signup'
                context = {'form':form,'message':message,'type_form':type_form}
                return render(request,'accounts/admin_stuff.html',context)
        
        else :
            form =  UserSignUpForm(request.GET)
            message = 'Invalid Credentials'
            type_form = 'signup'
            context = {'form':form,'message':message,'type_form':type_form}
            return render(request,'accounts/admin_stuff.html',context)

    else :
        form = UserSignUpForm(request.GET)
        message=''
        type_form='signup'
        class_list = get_list_or_404(Class)
        context = {'form':form,'message':message,'type_form':type_form,'class_list':class_list}
        return render(request,'accounts/admin_stuff.html',context)
