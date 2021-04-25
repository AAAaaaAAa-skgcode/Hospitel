from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class VaccineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaccine
        fields = ('id', 'brand', 'doses')

class SymptomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symptom
        fields = ('id', 'name')

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ('id', 'user_hospital', 'name', 'country',
        'city', 'street', 'number', 'postal_code', 'phone_number',
        'website')

class AvailableVaccinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailabeVaccines
        fields = ('id', 'hospital', 'vaccine', 'free_amount', 'reserved')

class VaccinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaccination
        fields = ('id','ssid', 'name', 'age', 'gender',
        'address', 'status', 'vaccine_brand', 'completed_doses',
        'symptoms', 'first_dose_date', 'second_dose_date',
        'hospital')
