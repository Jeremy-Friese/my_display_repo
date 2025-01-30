# f5_devices/models.py

from django.db import models

class F5DeviceModel(models.Model):
    name = models.CharField(max_length=100, unique=True)
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return self.name

