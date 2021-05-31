from django.urls import path
from . import views

urlpatterns = [
    path('',views.login,name="login"),
    path('register',views.register,name="register"),
    path('profile',views.hospital_profile,name="hospital_profile"),
    path('logout',views.logout_view,name="logout_view"),
    path('addVaccination',views.add_vaccination,name="add_vaccination"),
    path('updateVaccination/<str:amka>', views.update_vaccination, name='updateVaccination'),
    path('allVaccinations',views.all_vaccinations,name="all_vaccinations"),
        
    #path('resultdata',views.resultdata,name="resultdata"),
    #path('stats',views.stats,name="stats"),

    path('hospitalstats',views.hospitalstats,name="hospitalstats"),
    path('statsPerHospital',views.statsPerHospital,name="statsPerHospital"),
    path('countrystats',views.countrystats,name="countrystats"),
    path('statsPerCountry',views.statsPerCountry,name="statsPerCountry"),
    path('citystats',views.citystats,name="citystats"),
    path('statsPerCity',views.statsPerCity,name="statsPerCity"),
    path('agestats',views.agestats,name="agestats"),
    path('statsPerAge',views.statsPerAge,name="statsPerAge")

    
]
