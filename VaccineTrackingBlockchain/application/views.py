from django.http import HttpResponse
from .models import *
from .decorators import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login , logout
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
import re
import requests

# Create your views here.

@unauthenticated_user
def login(request):
    if request.method == 'POST':
        login_key = request.POST.get('login_key',False)
        if login_key == False:
            return register(request)
        username = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)

        if user is not None:
            auth_login(request,user)
            return redirect('hospital_profile')
        else:
            err = "Email or password is wrong."
            context = {'err':err}
            return render(request,'application/landing/index.html',context)
    return render(request,'application/landing/index.html')
@unauthenticated_user
def register(request):
    form = NewUserForm()
    err = None
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            try:
                User.objects.get(username=email)
            except User.DoesNotExist:
                user = User.objects.create_user(username=email,email=email,password = raw_password)
                hospital = Hospital.objects.create(
                        user = user,
                        name = request.POST.get('hospital-name'),
                        country = request.POST.get('country'),
                        city = request.POST.get('city'),
                        street = request.POST.get('street'),
                        number = request.POST.get('number'),
                        postal_code = request.POST.get('postal-code')
                )
                auth_login(request,user)
                return redirect("hospital_profile")
            err = "E-mail already exist."
            return render(request, 'application/landing/index.html',{'form':form,'err':err})
        else:
            err = form.errors
    
    return render(request, 'application/landing/index.html',{'form':form,'err':err})

@login_required(login_url="login")  
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url="login")
def hospital_profile(request):
    current_user = request.user
    current_hospital = Hospital.objects.get(user=current_user)
    context = {'current_hospital':current_hospital}
    return render(request, 'application/authenticated/profile.html',context)


