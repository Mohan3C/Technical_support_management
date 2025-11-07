from django.shortcuts import render,redirect
from django.contrib.auth import login,logout
from django.contrib.auth import authenticate
from itertools import chain

# app imports
from .models import User
from .form import *

# Create your views here.

def home(request):
    return render(request,"user/main.html")

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)
        
        if user is not None:
            login(request,user)

            if user.role == "agent":
                return redirect('agentdashboard')
            else:
                return redirect('homepage')
        else:
            return render(request,"registration/login.html",{'error': "Invalid username or password"})

    return render(request,"registration/login.html")

def registration(request):
    if request.method == "POST":
        username = request.POST.get('username')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        role = request.POST.get('role')
    
        if pass1==pass2:
            exist_user = User.objects.filter(username=username).exists()
            if exist_user:
                return render(request,"registration/register.html",{'error':"Username is already taken"})
            
            user = User()
            user.username = username
            user.set_password(pass1)
            user.role = role

            user.save()

            login(request,user)

            if user.role =="agent":
                return redirect('agentdashboard')
            else:
                return redirect('homepage')

    return render(request,"registration/register.html")

def user_logout(request):
    if request.method == "POST":
        logout(request)
        return redirect('homepage')
    
def user_dashboard(request):
    tickets = Ticket.objects.filter(created_by = request.user)
    comments = Comment.objects.filter(user = request.user)

    key = lambda obj:getattr(obj,'created_at',getattr(obj,'update',None))

    activities = sorted(chain(tickets,comments),key=key,reverse=True)

    for activity in activities:
        activity.model = activity.__class__.__name__

    open_tickets = tickets.filter(status="open")
    open_ticket_count = open_tickets.count()
    closed_ticket_count = tickets.filter(status="closed").count()
    total_ticket = tickets.count()
    recent_tickets = tickets.order_by('-created_at','-update')[:10]

    context = {
        "activities":activities,
        "open_tickets":open_tickets,
        "open_ticket":open_ticket_count,
        "closed_ticket":closed_ticket_count,
        "total_ticket":total_ticket,
        "recent_tickets":recent_tickets
    }
    return render(request,"user/dashboard.html",context)

def raise_ticket(request):
    form = TicketForm(request.POST or None,request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.save()
            
            return redirect('user_dashboard')
    
    return render(request,"user/raised_ticket.html",{"form":form})

def view_ticket(request):
    pass

def show_tickets(request):
    pass