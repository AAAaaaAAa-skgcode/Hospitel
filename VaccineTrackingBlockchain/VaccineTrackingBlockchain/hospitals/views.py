from .serializers import VaccinationSerializer
from django.shortcuts import render
from rest_framework import generics, status
from django.db import models
from .models import *
from .forms import *
from .decorators import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import  render, redirect
from django.contrib.auth import login, authenticate,logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

# Create your views here.

class VaccinationView(generics.CreateAPIView):
    queryset = Vaccination.objects.all()
    serializer_class = VaccinationSerializer

@unauthenticated_user
def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("dashboard")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="hospitals/login.html", context={"login_form":form})

@unauthenticated_user
def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("login")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm
	return render (request=request, template_name="hospitals/register.html", context={"register_form":form})

@login_required(login_url='login')
def dashboard(request):
    return render (request=request, template_name="hospitals/dashboard.html")

@login_required(login_url='login')
def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("login")