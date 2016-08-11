from django.contrib import admin

# Register your models here.


from .models import Client, SmsFac
from referral_system.models import  Appointment

admin.site.register(Client)
admin.site.register(SmsFac)
admin.site.register(Appointment)
