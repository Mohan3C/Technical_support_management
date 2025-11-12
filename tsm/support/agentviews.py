from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *

@login_required
def agent_dashboard(request):
    return render(request,"agent/dashboard.html")

@login_required
def agent_tickets(request):
    tickets = Ticket.objects.all()

    open_tickets = tickets.filter(status= "open").order_by("-created_at")
    progress_tickets = tickets.filter(assign_to = request.user,status ="progress").order_by("-update_at")

    priority_tickets = []
    priority =("urgent","high","medium","low")

    for p in priority:
        for t in open_tickets:
            if t.priority == p:
                priority_tickets.append(t)

    closed_tickets = tickets.filter(assign_to = request.user,status = "closed").order_by("-update_at")

    context = {
        "tickets":tickets,
        "open_tickets":open_tickets,
        "progress_tickets":progress_tickets,
        "priority_tickets":priority_tickets,
        "closed_tickets":closed_tickets
    }

    return render(request,"agent/ticket.html",context)

@login_required
def take_ticket(request,id):
    ticket = Ticket.objects.get(id=id)
    ticket.assign_to = request.user
    ticket.status = "progress"
    ticket.save()
    return render(request,"agent/agent_view_ticket.html",{"ticket":ticket})

@login_required
def close_ticket(request,id):
    ticket = Ticket.objects.get(id=id)
    ticket.status = "closed"
    ticket.save()

    return redirect("agent_view_ticket",id=id)

@login_required
def agent_view_ticket(request,id):
    ticket = Ticket.objects.get(id=id)
   
    comments = Comment.objects.filter(ticket=ticket).order_by("created_at")

    return render(request,"agent/agent_view_ticket.html",{"ticket":ticket,"comments":comments})


@login_required
def agent_comment(request,id):
    print("It come here and gone. I don`t know where it goes")
    if request.method == "POST":
        comment = request.POST.get('comment')
        ticket = get_object_or_404(Ticket,id=id)

        if comment:
            if not ticket.assign_to :
                ticket.assign_to = request.user
                ticket.status = "progress"
                ticket.save()

            obj = Comment()
            obj.ticket = ticket
            obj.user = request.user
            obj.content = comment
            obj.save()

            return redirect("agent_view_ticket",id=ticket.id)
    
    return redirect("agent_view_ticket",id=id)



def in_progress_ticket(request):
    return render(request,"agent/progress.html")

def agent_closed_ticket(request):
    return render(request,"agent/closed.html")

def agent_setting(request):
    return render(request,"agent/agentsetting.html")