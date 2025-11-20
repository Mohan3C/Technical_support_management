from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from itertools import chain


from .models import *
from .decorators import permission_check

@login_required
@permission_check(role="agent")
def agent_dashboard(request):
    tickets = Ticket.objects.filter(assign_to = request.user)
    comments = Comment.objects.filter(user=request.user)

    key = lambda obj:getattr(obj,"created_at",getattr(obj,"update_at",None))

    activities = sorted(chain(tickets,comments),key=key,reverse=True)[:20]

    for activity in activities:
        activity.model = activity.__class__.__name__

    progress_tickets = tickets.filter(status="progress")
    closed_tickets = tickets.filter(status="closed")
    recent_tickets = tickets.order_by("-update_at")[:10]

    print(f"activities: {activities}")
    

    context = {
        "tickets":tickets,
        "progress_tickets":progress_tickets,
        "closed_tickets":closed_tickets,
        "recent_tickets":recent_tickets,
        "activities":activities,
    }

    return render(request,"agent/dashboard.html",context)

@login_required
@permission_check(role="agent")
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
@permission_check(role="agent")
def take_ticket(request,id):
    ticket = Ticket.objects.get(id=id)
    ticket.assign_to = request.user
    ticket.status = "progress"
    ticket.save()
    return render(request,"agent/agent_view_ticket.html",{"ticket":ticket})

@login_required
@permission_check(role="agent")
def close_ticket(request,id):
    ticket = Ticket.objects.get(id=id)
    ticket.status = "closed"
    ticket.save()

    return redirect("agent_view_ticket",id=id)

@login_required
@permission_check(role="agent")
def agent_view_ticket(request,id):
    ticket = Ticket.objects.get(id=id)
   
    comments = Comment.objects.filter(ticket=ticket).order_by("created_at")

    return render(request,"agent/agent_view_ticket.html",{"ticket":ticket,"comments":comments})


@login_required
@permission_check(role="agent")
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


@login_required
@permission_check(role="agent")
def in_progress_ticket(request):
    return render(request,"agent/progress.html")

@login_required
@permission_check(role="agent")
def agent_setting(request):
    return render(request,"agent/agentsetting.html")