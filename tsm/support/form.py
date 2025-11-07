from .models import *
from django.forms import ModelForm

class TicketForm(ModelForm):

    class Meta:
        model = Ticket
        fields = ["problem_type","title","description","image"]