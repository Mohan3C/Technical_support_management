from django.db import models
from django.shortcuts import render, redirect,get_object_or_404
from .models import User,Ticket,Comment

def admin_dashboard(request):
    customer = User.objects.filter(role="customer")
    agent = User.objects.filter(role="agent")

    ticket = Ticket.objects.all()
    open_ticket_count = ticket.filter(status = "open").count()
    closed_ticket_count = ticket.filter(status="closed").count()
    progress_ticket_count = ticket.filter(status="progress").count()

    context = {
        "customer":customer,
        "agent":agent,
        "ticket":ticket,
        "open_ticket_count":open_ticket_count,
        "closed_ticket_count":closed_ticket_count,
        "progress_ticket_count":progress_ticket_count,
    }

    return render(request,"adminuser/dashboard.html",context)

def manageticket(request):
    tickets = Ticket.objects.all()
    open_tickets = tickets.filter(status="open").order_by("created_at")
    closed_tickets = tickets.filter(status="closed").order_by("-update_at")
    progress_tickets = tickets.filter(status="progress").order_by("-update_at")
    tickets_by_priority = tickets.filter(status = "open").order_by("-status")

    context = {
        "tickets":tickets,
        "open_tickets":open_tickets,
        "closed_tickets":closed_tickets,
        "progress_tickets":progress_tickets,
        "tickets_by_priority":tickets_by_priority,
    }

    return render(request,"adminuser/manageticket.html",context)

def manageuser(request):
    customers = User.objects.filter(role="customer")
    
    for customer in customers:
        total_tickets = Ticket.objects.filter(created_by = customer)
        customer.total_tickets = total_tickets.count()
        customer.open_tickets_count = total_tickets.filter(status="open").count()
        customer.progress_tickets_count = total_tickets.filter(status="progress").count()
        customer.closed_tickets_count = total_tickets.filter(status="closed").count()

    context={
        "customers":customers,
    }

    return render(request,"adminuser/manageUser.html",context)

def view_user(request,user_id):
    customer = User.objects.get(id=user_id)
    agents = User.objects.filter(role="agent")

    tickets = Ticket.objects.filter(created_by=customer)
    open_tickets = tickets.filter(status="open")
    progress_tickets = tickets.filter(status="progress")
    closed_tickets = tickets.filter(status="closed")

    context={
       "customer":customer,
       "open_tickets":open_tickets,
       "progress_tickets":progress_tickets,
       "closed_tickets":closed_tickets,
       "agents":agents
    }

    return render(request,"adminuser/view_user.html",context)

def admin_view_ticket(request,id):
    ticket = Ticket.objects.get(id=id)

    comments = Comment.objects.filter(ticket=ticket)

    return render(request,"adminuser/view_ticket.html",{"ticket":ticket,"comments":comments})

def report(request):
    return render(request,"adminuser/report.html")

def manageAgent(request):
    agents = User.objects.filter(role="agent")

    for agent in agents:
        tickets = Ticket.objects.filter(assign_to = agent)

        agent.tickets = tickets.count()
        agent.progress_tickets = tickets.filter(status="progress").count()
        agent.closed_tickets = tickets.filter(status="closed").count()

    return render(request,"adminuser/manageAgent.html",{"agents":agents})

def view_agent(request,agent_id):
    agent = User.objects.get(id=agent_id)

    tickets = Ticket.objects.filter(assign_to = agent)

    progress_tickets = tickets.filter(status="progress")
    closed_tickets = tickets.filter(status="closed")

    context = {
        "agent":agent,
        "tickets":tickets,
        "progress_tickets":progress_tickets,
        "closed_tickets":closed_tickets,
    }

    return render(request,"adminuser/view_agent.html",context)

def assign_agent(request,id):
    ticket = Ticket.objects.get(id=id)

    user_id=ticket.created_by.id

    if request.method == "POST":
        assign_to = request.POST.get("userId")
        if assign_to :
            agent = get_object_or_404(User,id=assign_to)
            ticket.assign_to = agent
            ticket.status = "progress"

            ticket.save()
        
        return redirect("view_customer",user_id)
   
    return render(request,"adminuser/assign.html")


def admin_take(request,id):
    ticket = Ticket.objects.get(id=id)

    ticket.assign_to = request.user
    ticket.save()
    user_id = ticket.created_by.id

    return redirect("view_customer",user_id)