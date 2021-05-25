from django.http import HttpResponse, JsonResponse
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
import json

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
                pfizer_vaccine = Vaccine.objects.get(brand='Pfizer')
                avail_pfizer = AvailabeVaccines.objects.create(
                    hospital = hospital,
                    vaccine = pfizer_vaccine
                )
                moderna_vaccine = Vaccine.objects.get(brand='Moderna')
                avail_pfizer = AvailabeVaccines.objects.create(
                    hospital = hospital,
                    vaccine = moderna_vaccine
                )
                johnson_vaccine = Vaccine.objects.get(brand='Johnson & Johnson')
                avail_pfizer = AvailabeVaccines.objects.create(
                    hospital = hospital,
                    vaccine = johnson_vaccine
                )
                astra_vaccine = Vaccine.objects.get(brand='AstraZeneca')
                avail_pfizer = AvailabeVaccines.objects.create(
                    hospital = hospital,
                    vaccine = astra_vaccine
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
    
    pfizer_vaccine = Vaccine.objects.get(brand='Pfizer')
    current_pfizer = AvailabeVaccines.objects.get(hospital=current_hospital, vaccine = pfizer_vaccine)
    
    moderna_vaccine = Vaccine.objects.get(brand='Moderna')
    current_moderna = AvailabeVaccines.objects.get(hospital=current_hospital, vaccine = moderna_vaccine)
    
    johnson_vaccine = Vaccine.objects.get(brand='Johnson & Johnson')
    current_johnson = AvailabeVaccines.objects.get(hospital=current_hospital, vaccine = johnson_vaccine)
    
    astra_vaccine = Vaccine.objects.get(brand='AstraZeneca')
    current_astra = AvailabeVaccines.objects.get(hospital=current_hospital, vaccine = astra_vaccine)

    if request.method=="POST":
        name = request.POST.get('hospital-name')
        country = request.POST.get('country')
        city = request.POST.get('city')
        street = request.POST.get('street')
        number = request.POST.get('number')
        postal_code = request.POST.get('postal-code')
        email = request.POST.get('email')
        
        pfizer_avail_doses = request.POST.get('pfizer-doses')
        moderna_avail_doses = request.POST.get('moderna-doses')
        johnson_avail_doses = request.POST.get('johnson-doses')
        astra_avail_doses = request.POST.get('astra-doses')

        current_user.email = email
        current_hospital.name = name
        current_hospital.country = country
        current_hospital.city = city
        current_hospital.street = street
        current_hospital.number = number
        current_hospital.postal_code = postal_code
        
        current_pfizer.free_amount = pfizer_avail_doses
        current_moderna.free_amount = moderna_avail_doses
        current_johnson.free_amount = johnson_avail_doses
        current_astra.free_amount = astra_avail_doses

        current_pfizer.save()
        current_moderna.save()
        current_johnson.save()
        current_astra.save()
        
        current_user.save()
        current_hospital.save()

        context = {'current_hospital':current_hospital, 'current_pfizer':current_pfizer,'current_moderna':current_moderna, 'current_johnson':current_johnson, 'current_astra':current_astra}
        return redirect("/profile")

    context = {'current_hospital':current_hospital, 'current_pfizer':current_pfizer,'current_moderna':current_moderna, 'current_johnson':current_johnson, 'current_astra':current_astra}
    return render(request, 'application/authenticated/profile.html',context)

def add_vaccination(request):
    current_user = request.user
    current_hospital = Hospital.objects.get(user=current_user)

    if request.method=="POST":
        ssid = request.POST.get('amka')
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lastname')
        gender = request.POST.get('mySelect')
        age = request.POST.get('age')
        address = request.POST.get('street')
        city = request.POST.get('city')
        country = request.POST.get('country')
        postal_code = request.POST.get('postal-code')
        vbrand = request.POST.get('vbrand')
        dose_a = request.POST.get('dosea')
        dose_b = request.POST.get('doseb')
        completed_doses = request.POST.get('compldoses')
        status = request.POST.get('status')
        symptoms = request.POST.get('symptoms')

        try:
            vaccine_brand = Vaccine.objects.get(brand=vbrand)
            current_hospital.amount = current_hospital.amount + 1
            print(current_hospital.amount)
            current_hospital.save()
        except Vaccine.DoesNotExist:
            context = {'err':"Κάτι πήγε στραβά 🍌"}
            return render(request, 'application/authenticated/add_vaccination.html',context)

        vaccination = Vaccination.objects.create(
            ssid = ssid,
            first_name = first_name,
            last_name = last_name,
            age = age,
            gender = gender,
            address = address,
            city = city,
            country = country,
            postal_code = postal_code,
            status = status,
            vaccine_brand = vaccine_brand,
            completed_doses = completed_doses,
            symptoms = symptoms,
            first_dose_date = dose_a,
            second_dose_date = dose_b,
            hospital = current_hospital
        )
        if vaccination == None:
            context = {'err':"Κάτι πήγε στραβά"}
            return render(request, 'application/authenticated/add_vaccination.html',context)
        return redirect("/addVaccination")

    return render(request, 'application/authenticated/add_vaccination.html')



@login_required(login_url="login")
def stats(request):
    return render(request,'application/authenticated/stats.html')

def resultdata(request):
    data = {}
   
    for hosp in Hospital.objects.filter():
        data[hosp.name] = hosp.amount
        print('data',data)
    

    return JsonResponse(data, safe=False)



@login_required(login_url="login")
def statsPerCountrie(request):
    return render(request,'application/authenticated/countriesStats.html')

def countriesstats(request):

    data = {}
   
    for hosp in Hospital.objects.filter():
        data[hosp.country] = hosp.amount
        print('data',data)
    

    return JsonResponse(data, safe=False)
    

@login_required(login_url="login")
def statsPerCity(request):
    return render(request,'application/authenticated/cityStats.html')

def citystats(request):

    data = {}
   
    for hosp in Hospital.objects.filter():
        data[hosp.city] = hosp.amount
        print('data',data)
    

    return JsonResponse(data, safe=False)
    
