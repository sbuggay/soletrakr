from django.contrib.gis import admin as gis_admin

from .models import Path, Geofence


gis_admin.site.register(Path, gis_admin.GeoModelAdmin)
gis_admin.site.register(Geofence, gis_admin.GeoModelAdmin)