from django.shortcuts import render,redirect
from django.contrib.auth import login,logout
from django.contrib.auth import authenticate
from .models import User

# Create your views here.

def home(request):
    return render(request,"user/dashboard.html")

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
    
def ticket(request):
    return render(request,"user/ticket.html")