# f5_devices/admin.py

from django.contrib import admin
from .models import F5DeviceModel

@admin.register(F5DeviceModel)
class F5DeviceAdmin(admin.ModelAdmin):
    """
    Admin interface for F5 Devices.
    """
    list_display = ("name", "ip_address")
    search_fields = ("name", "ip_address")
    list_filter = ("ip_address",)

