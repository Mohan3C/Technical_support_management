from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from itertools import chain

# app imports
from .models import User
from .form import *

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        if request.user.role == "agent":
            logout(request)

    return render(request,"user/main.html")


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)
        
        if user is not None:
            login(request,user)

            if user.role == "agent":
                return redirect('agent_dashboard')
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
                return redirect('agent_dashboard')
            else:
                return redirect('homepage')

    return render(request,"registration/register.html")

def user_logout(request):
    if request.method == "POST":
        logout(request)
        return redirect('homepage')
    
@login_required
def user_dashboard(request):
    tickets = Ticket.objects.filter(created_by = request.user)
    comments = Comment.objects.filter(user = request.user)

    key = lambda obj:getattr(obj,'created_at',getattr(obj,'update_at',None))

    activities = sorted(chain(tickets,comments),key=key,reverse=True)

    for activity in activities:
        activity.model = activity.__class__.__name__

    open_tickets = tickets.filter(status="open")
    open_ticket_count = open_tickets.count()
    closed_ticket_count = tickets.filter(status="closed").count()
    total_ticket = tickets.count()
    recent_tickets = tickets.order_by('-created_at','-update_at')[:10]

    context = {
        "activities":activities,
        "open_tickets":open_tickets,
        "open_ticket":open_ticket_count,
        "closed_ticket":closed_ticket_count,
        "total_ticket":total_ticket,
        "recent_tickets":recent_tickets
    }
    return render(request,"user/dashboard.html",context)

@login_required
def raise_ticket(request):
    form = TicketForm(request.POST or None,request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.save()
            
            return redirect('user_dashboard')
    
    return render(request,"user/raised_ticket.html",{"form":form})

@login_required
def view_ticket(request,id):
    ticket  = Ticket.objects.get(id=id,created_by = request.user)

    comments = ticket.comments.all().order_by("created_at")

    status = ticket.status
    progress = None
    closed_ticket = None
    if status == "progress":
        progress = True
    elif status == "closed":
        closed_ticket = True

    context = {
        "ticket":ticket,
        "comments":comments,
        "progress":progress,
        "closed_ticket":closed_ticket
    }
    return render(request,"user/view_ticket.html",context)

@login_required
def show_tickets(request):
    tickets = Ticket.objects.filter(created_by = request.user).order_by("-created_at")

    return render(request,"user/all_ticket.html",{"tickets":tickets})

@login_required
def comment(request,id):
    if request.method == "POST":
        comment = request.POST.get('comment')
        ticket = Ticket.objects.get(id=id)
        if comment:
            obj = Comment()
            obj.ticket = ticket
            obj.user = request.user
            obj.content = comment
            obj.save()

            return redirect("view_ticket",id=ticket.id)
    
    return redirect("view_ticket",id=id)

@login_required
def reopen_ticket(request,id):
    ticket = get_object_or_404(Ticket,id=id)

    new_ticket = Ticket()
    new_ticket.created_by = request.user
    new_ticket.title = ticket.title
    new_ticket.description = ticket.description
    new_ticket.problem_type = ticket.problem_type
    new_ticket.priority = ticket.priority
    new_ticket.save()

    return redirect("user_dashboard")

def profile(request):
    return render(request,"registration/profile.html")




