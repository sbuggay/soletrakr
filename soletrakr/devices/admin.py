from django.contrib import admin
from django.contrib.gis import admin as gis_admin

from devices.models import Device


class DeviceAdmin(admin.ModelAdmin):
	"""
	Register devices on Django admin site.
	"""
	pass

gis_admin.site.register(Device, gis_admin.GeoModelAdmin)