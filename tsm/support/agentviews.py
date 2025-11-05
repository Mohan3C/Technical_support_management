from django.shortcuts import render
from .models import *

def dashboard(request):
    return render(request,"agent/dashboard.html")