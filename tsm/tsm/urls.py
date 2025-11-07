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

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",home,name="homepage"),
    path("registration/",registration,name="registration"),
    path("login/",user_login,name="login"),
    path("logout/",user_logout,name="logout"),
    path("ticket/",ticket,name="ticket"),


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
