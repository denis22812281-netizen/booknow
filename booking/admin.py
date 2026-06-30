from django.contrib import admin
from .models import Service, Master, Appointment


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'duration', 'price', 'icon']


@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ['name', 'specialization']


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'client_phone', 'service', 'master', 'date', 'time', 'status']
    list_filter = ['status', 'date', 'service', 'master']
    list_editable = ['status']
    search_fields = ['client_name', 'client_phone']
    date_hierarchy = 'date'
