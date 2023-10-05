# Register your models here.
from django.contrib import admin
from .models import Destination, Trip

admin.site.register(Destination)
admin.site.register(Trip)
