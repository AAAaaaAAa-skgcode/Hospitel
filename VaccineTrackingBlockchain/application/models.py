from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Hospital(models.Model):
    user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=200,default="",blank=True,null=True)
    address = models.CharField(max_length=200,default="",blank=True,null=True)
    country = models.CharField(max_length=200,default="",blank=True,null=True)
    city = models.CharField(max_length=200,default="",blank=True,null=True)
    street = models.CharField(max_length=200,default="",blank=True,null=True)
    number = models.IntegerField(default=-1,blank=True,null=True)
    postal_code = models.IntegerField(default=-1,blank=True,null=True)
    def __str__(self):
        return (self.name)

class Vaccine(models.Model):
    brand = models.CharField(max_length=200,default="",blank=True,null=True)
    doses = models.IntegerField(default=-1,blank=True,null=True)

class AvailabeVaccines(models.Model):
    hospital = models.ForeignKey(Hospital,on_delete=models.CASCADE)
    vaccine = models.ForeignKey(Vaccine,on_delete=models.CASCADE)
    free_amount = models.IntegerField(default=-1,blank=True,null=True)
    reserved = models.IntegerField(default=-1,blank=True,null=True)

#vaccination local
status_vaccination = [
    ("pending", "pending"),
    ("completed", "completed"),
    ("cancelled", "cancelled"),
]

number_of_doses = [
    (0, 0),
    (1, 1),
    (2, 2),
]

class Vaccination(models.Model):
    ssid = models.CharField(max_length=200,default="",blank=True,null=True)
    name = models.CharField(max_length=200,default="",blank=True,null=True)
    age = models.IntegerField(default=-1,blank=True,null=True)
    gender = models.BooleanField(default=False)
    address = models.CharField(max_length=200,default="",blank=True,null=True)
    status = models.CharField(max_length=50, choices=status_vaccination , default="pending")
    vaccine_brand = models.ForeignKey(Vaccine,on_delete=models.CASCADE)
    completed_doses = models.IntegerField(choices=number_of_doses , default=0)
    symptoms = models.CharField(max_length=2000,default="",blank=True,null=True)
    first_dose_date = models.DateField(null=True)
    second_dose_date = models.DateField(null=True)
    hospital = models.ForeignKey(Hospital,on_delete=models.CASCADE)
