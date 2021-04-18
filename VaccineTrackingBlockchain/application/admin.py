from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Hospital)
admin.site.register(Vaccine)
admin.site.register(AvailabeVaccines)
admin.site.register(Vaccination)