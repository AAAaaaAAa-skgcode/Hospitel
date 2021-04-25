from django.db import models
from django.contrib.auth.models import User

class Vaccine(models.Model):
    COMPANIES = (
        ('Pfizer', 'Pfizer'),
        ('AstraZeneca', 'AstraZeneca'),
        ('Moderna', 'Moderna'),
        ('Sputink', 'Sputink'),
        ('Johnson & Johnson', 'Johnson & Johnson')
    )
    brand = models.CharField(max_length=200,default="",blank=True, null=True, choices = COMPANIES)
    doses = models.IntegerField(default=-1,blank=True,null=True)

    def __str__(self):
        if self.brand==None:
            return ""
        return self.brand


class Symptom(models.Model):
    name = models.CharField(max_length=200,default="",blank=True,null=True)
    def __str__(self):
        if self.name==None:
            return ""
        return self.name




class Hospital(models.Model):
    user_hospital = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=200,default="",blank=True,null=True)
    country = models.CharField(max_length=200,default="",blank=True, null=True)
    city = models.CharField(max_length=200,default="",blank=True, null=True)
    street = models.CharField(max_length=200,default="",blank=True, null=True)
    number = models.IntegerField(default=-1,blank=True,null=True)
    postal_code = models.IntegerField(default=-1,blank=True, null=True)
    phone_number = models.CharField(max_length=200,default="",blank=True,null=True)
    website = models.CharField(max_length=200,default="",blank=True,null=True)

    def __str__(self):
        if self.name==None:
            return ""
        return self.name




class AvailabeVaccines(models.Model):
    hospital = models.ForeignKey(Hospital,on_delete=models.CASCADE)
    vaccine = models.ForeignKey(Vaccine,on_delete=models.CASCADE)
    free_amount = models.IntegerField(default=-1,blank=True,null=True)
    reserved = models.IntegerField(default=-1,blank=True,null=True)

    def __str__(self):
        return (str(self.hospital) + " " + str(self.vaccine))

    # free + reserved = total


#vaccination local
status_vaccination = [
    ("Pending", "Pending"),
    ("Completed", "Completed"),
    ("Cancelled", "Cancelled"),
]

number_of_doses = [
    (0, 0),
    (1, 1),
    (2, 2),
]

genders = [
    ("Male", "Male"),
    ("Female", "Female"),
    ("Other", "Other"),
]


class Vaccination(models.Model):
    ssid = models.CharField(max_length=200,default="",blank=True,null=True)
    name = models.CharField(max_length=200,default="",blank=True,null=True)
    age = models.IntegerField(default=-1,blank=True,null=True)
    gender = models.CharField(max_length=50, choices=genders , default="pending")
    address = models.CharField(max_length=200,default="",blank=True,null=True)
    status = models.CharField(max_length=50, choices=status_vaccination , default="pending")
    vaccine_brand = models.ForeignKey(Vaccine,on_delete=models.CASCADE)
    completed_doses = models.IntegerField(choices=number_of_doses , default=0)
    symptoms = models.ManyToManyField(Symptom,null=True,blank=True)
    first_dose_date = models.DateField(null=True)
    second_dose_date = models.DateField(null=True)
    hospital = models.ForeignKey(Hospital,on_delete=models.CASCADE)
