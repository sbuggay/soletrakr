from tastypie import fields
from tastypie.contrib.gis.resources import ModelResource
from tastypie.resources import ALL, ALL_WITH_RELATIONS#, ModelResource
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized
from tastypie.throttle import CacheThrottle

from devices.api import DeviceResource

from .models import Path, Geofence


class PathResource(ModelResource):
	"""
	API resource for path models.
	"""
	device = fields.ToOneField('devices.api.DeviceResource', 'device')
	
	class Meta:
		queryset = Path.objects.all()
		resource_name = 'paths'
		allowed_methods = ['get', 'patch']
		authentication = ApiKeyAuthentication()
		authorization = Authorization() #AttachedUserAuthorization()
		throttle = CacheThrottle(throttle_at=1, timeframe=2) # throttle at 1 request per 2 seconds
		include_resource_uri = True
		fields = ['points',]


class GeofenceResource(ModelResource):
	"""
	API resource for geofence models.
	"""
	device = fields.ToOneField('devices.api.DeviceResource', 'device')

	class Meta:
		queryset = Geofence.objects.all()
		resource_name = 'geofences'
		allowed_methods = ['get', 'patch']
		authentication = ApiKeyAuthentication()
		authorization = Authorization()
		throttle = CacheThrottle(throttle_at=1, timeframe=2)
		include_resource_uri = True
		fields = ['area',]