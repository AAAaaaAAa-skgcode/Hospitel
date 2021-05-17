from django.urls import path
from . import views

urlpatterns = [
    path('',views.login,name="login"),
    path('register',views.register,name="register"),
    path('profile',views.hospital_profile,name="hospital_profile"),
    path('logout',views.logout_view,name="logout_view"),
    path('addVaccination',views.add_vaccination,name="add_vaccination")
    
]
