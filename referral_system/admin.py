from django.contrib import admin

# Register your models here.


from .models import Client, SmsFac
from referral_system.models import Service, Appointment

admin.site.register(Client)
admin.site.register(SmsFac)
admin.site.register(Service)
admin.site.register(Appointment)
