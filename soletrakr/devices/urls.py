from django.conf.urls import patterns, url, include

from devices.api import *

urlpatterns = patterns('devices.views',

	# Device creation/activation
	url(r'^devices/create/$', 'create_device', name='create_device'),
	url(r'^devices/activate/$', 'activate_device', name='activate_device'),

	# Device-related API URIs
	url(r'^api/', include(DeviceResource().urls)),
)