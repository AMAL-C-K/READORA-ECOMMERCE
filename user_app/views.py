from django.shortcuts import render,redirect
from .forms import RegisterForm,LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
import re

def signUp(request):
    if request.method =='POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            firstname=form.cleaned_data['first_name']
            lastname= form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']


            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already exist")
                return render(request, "signup.html", {'form': form})
            elif User.objects.filter(username=username).exists():
                messages.error(request, "Username is already Exists")
                return render(request, "signup.html", {'form': form})
            elif not re.fullmatch(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,}$', password):
                messages.error(request, 'password should be mix of  (0-9),(a-z),(A-Z) special characters ')
                return render(request, "signup.html", {'form': form})
            elif password!=confirm_password:
                messages.error(request,'Password not matching')
                return render(request, "signup.html", {'form': form})
            else:
                user = User(first_name=firstname,last_name=lastname,email=email,username=username)
                user.set_password(password)                                                    #password hashing
                user.save()
                login(request,user)
                return redirect('home')
    
    else:
        form = RegisterForm()
    return render(request,"signup.html",{'form':form})

def signIn(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username,password=password)
            if user:
                login(request,user)
                return redirect('home')
            else:
                messages.error(request, "invalid credentials")
    else:
        form = LoginForm()

    return render(request, "signin.html",{'form':form})

def signOut(request):
    logout(request)
    return redirect('home')