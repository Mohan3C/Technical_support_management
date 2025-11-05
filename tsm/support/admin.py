from django.contrib import admin
from .models import *

# Register your models here.

admin.site.site_title ="TSM"
admin.site.site_header = "Technical Support Management"
admin.site.index_title = "TSM Site"

admin.site.register(User)
admin.site.register(Ticket)
admin.site.register(Comment)