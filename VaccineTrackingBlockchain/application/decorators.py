from django.http import HttpResponse
from django.shortcuts import redirect
from .models import *



def unauthenticated_user(view_func):
    def wrapper_func(request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('hospital_profile')
        else:
            return view_func(request,*args, **kwargs)
    return wrapper_func
