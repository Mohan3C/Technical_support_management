from django.db import models
from django.shortcuts import render, redirect

def admin_dashboard(request):
    return render(request,"admin/dashboard.html")

def manageticket(request):
    return render(request,"admin/manageticket.html")

def manageuser(request):
    return render(request,"admin/manageUser.html")

def report(request):
    return render(request,"admin/report.html")

def manageAgent(request):
    return render(request,"admin/manageAgent")