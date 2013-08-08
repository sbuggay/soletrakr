from django.conf.urls import patterns, url, include

from .api import PathResource, GeofenceResource

urlpatterns = patterns('maps.views',
	url(r'^api/', include(PathResource().urls)),
	url(r'^api/', include(GeofenceResource().urls)),
)