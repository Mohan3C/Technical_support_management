"""
URL configuration for tsm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from support.views import *
from support.agentviews import *
from support.adminviews import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # login urls 
    path("registration/",registration,name="registration"),
    path("login/",user_login,name="login"),
    path("logout/",user_logout,name="logout"),

    # user urls 
    path("",home,name="homepage"),
    path("dashboard/",user_dashboard,name="user_dashboard"),
    path("Ticket/New",raise_ticket,name="raised_ticket"),
    path("all_Ticket/",show_tickets,name="all_tickets"),
    path("Ticket/view/<int:id>/",view_ticket,name="view_ticket"),
    path("Ticket/view/comment/<int:id>/",comment,name="comment"),


    # agent urls
    path("agent/dashboard",agent_dashboard,name="agent_dashboard"),
    path("agent/ticket",agent_ticket,name="agent_ticket"),
    path("agent/progess_ticket",in_progress_ticket,name="agent_progress_ticket"),
    path("agent/closed_ticket",agent_closed_ticket,name="agent_closed_ticket"),
    path("agent/setting",agent_setting,name="agentsetting"),

    # admin urls
    path("admin/dashboard/",admin_dashboard,name="admindashboard"),
    path("admin/manage_ticket/",manageticket,name="adminticket"),
    path("admin/manage_agent/",manageAgent,name="adminagent"),
    path("admin/manage_report/",report,name="report"),
    path("admin/manage_user/",manageuser,name="manageUser")

]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)