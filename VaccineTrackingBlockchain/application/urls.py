from django.urls import path
from . import views

urlpatterns = [
    path('',views.login,name="login"),
    path('register',views.register,name="register"),
    path('profile',views.hospital_profile,name="hospital_profile"),
    path('logout',views.logout_view,name="logout_view"),
    path('addVaccination',views.add_vaccination,name="add_vaccination"),
        
    path('resultdata',views.resultdata,name="resultdata"),
    path('stats',views.stats,name="stats"),
    path('countriesstats',views.countriesstats,name="countriesstats"),
    path('statsPerCountrie',views.statsPerCountrie,name="statsPerCountrie"),
    path('citystats',views.citystats,name="citystats"),
    path('statsPerCity',views.statsPerCity,name="statsPerCity")

    
]
