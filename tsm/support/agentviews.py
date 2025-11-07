from django.shortcuts import render
from .models import *

def agent_dashboard(request):
    return render(request,"agent/dashboard.html")

def agent_ticket(request):
    return render(request,"agent/ticket.html")

def in_progress_ticket(request):
    return render(request,"agent/progress.html")

def agent_closed_ticket(request):
    return render(request,"agent/closed.html")

def agent_setting(request):
    return render(request,"agent/agentsetting.html")