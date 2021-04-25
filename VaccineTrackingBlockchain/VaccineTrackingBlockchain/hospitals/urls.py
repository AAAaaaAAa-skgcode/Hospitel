from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path("", views.login_request, name="login"),
    path("register", views.register_request, name="register"),
    path('api/vaccination',VaccinationView.as_view()),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("logout", views.logout_request, name= "logout"),
    
]
  