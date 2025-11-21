from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.


class Ticket(models.Model):
    statu_choice = (
        ('open','open'),
        ('progress','progress'),
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
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    ticket = models.ForeignKey(Ticket,on_delete=models.CASCADE,related_name="comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True)
    content = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='comment_attachments/',blank=True,null=True)

    def __str__(self):
        return f"comment by {self.user.username}"
    
class User(AbstractUser):
    role_choice = (
        ('customer','customer'),
        ('agent','agent'),
        ('senior_agent','senior_agent')
    )
    role = models.CharField(max_length=20,choices=role_choice,default="customer")
    name = models.CharField(max_length=200,null=True,blank=True)
    phone_no = models.CharField(max_length=15, null=True, blank=True)
    image = models.ImageField(upload_to="profile/",blank=True,null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"
    
class TicketAttachment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='ticket_attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.uploaded_by.username