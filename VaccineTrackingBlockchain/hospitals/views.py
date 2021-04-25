from .serializers import VaccinationSerializer
from django.shortcuts import render
from rest_framework import generics, status
from django.db import models
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.

class VaccinationView(generics.CreateAPIView):
    queryset = Vaccination.objects.all()
    serializer_class = VaccinationSerializer


