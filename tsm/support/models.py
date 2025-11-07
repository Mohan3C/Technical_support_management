from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.


class Ticket(models.Model):
    statu_choice = (
        ('open','open'),
        ('in_progess','in_progress'),
        ('solved','solved'),
        ('closed','closed')
    )

    priority_choice = (
        ('low','low'),
        ('medium','medium'),
        ('high','high'),
        ('urgent','urgent')
    )

    problem_type = (
        ('support','support'),
        ('technical','technical'),
        ('sells','sells'),
        ('deployment','deployment'),
    )

    problem_type = models.CharField(max_length=20,choices=problem_type)
    title = models.CharField(max_length=300)
    description = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="created_ticket")
    assign_to = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,blank=True,null=True,related_name="assigned_ticket")
    status = models.CharField(max_length=20,choices=statu_choice,default="open")
    priority = models.CharField(max_length=20,choices=priority_choice,default="medium")
    created_at = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="Image/",blank=True,null=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    ticket = models.ForeignKey(Ticket,on_delete=models.CASCADE,related_name="comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"comment by {self.user.username}"
    
class User(AbstractUser):
    role_choice = (
        ('customer','customer'),
        ('agent','agent'),
        ('senior_agent','senior_agent')
    )
    role = models.CharField(max_length=20,choices=role_choice,default="customer")

    def __str__(self):
        return f"{self.username} ({self.role})"