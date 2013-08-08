from tastypie import fields
from tastypie.contrib.gis.resources import ModelResource
from tastypie.resources import ALL, ALL_WITH_RELATIONS#, ModelResource
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized
from tastypie.throttle import CacheThrottle

from devices.models import Device
from users.api import UserResource


class AttachedUserAuthorization(Authorization):
	"""
	Custom API Authorization to enforce users only being
	able to see the devices attached to their account.

	Implemented according to Tastypie documentation:
	================================================
	https://django-tastypie.readthedocs.org/en/latest/authorization.html

	@param object_list: 	queryset from DeviceResource class
	@param bundle: 			bundle object to get request.user
	"""
	def read_list(self, object_list, bundle):
		return object_list.filter(user=bundle.request.user)

	def read_detail(self, object_list, bundle):
		return bundle.obj.user == bundle.request.user

	def update_list(self, object_list, bundle):
		return object_list.filter(user=bundle.request.user)

	def update_detail(self, object_list, bundle):
		return bundle.obj.user == bundle.request.user

	def create_list(self, object_list, bundle):
		raise Unauthorized("Creation not authorized.")

	def create_detail(self, object_list, bundle):
		raise Unauthorized("Creation not authorized.")

	def delete_list(self, object_list, bundle):
		raise Unauthorized("Deletion not authorized.")

	def delete_detail(self, object_list, bundle):
		raise Unauthorized("Deletion not authorized.")


class DeviceResource(ModelResource):
	"""
	Resource class to setup URI endpoints for
	users for REST API.
	"""
	path = fields.ToOneField('maps.api.PathResource', 'path')

	class Meta:
		queryset = Device.objects.filter(is_active=True)
		resource_name = 'devices'
		allowed_methods = ['get', 'patch']
		authentication = ApiKeyAuthentication()
		authorization = AttachedUserAuthorization()
		throttle = CacheThrottle(throttle_at=1, timeframe=2) # throttle at 1 request per 2 seconds
		collection_name = 'devices'
		include_resource_uri = True
		detail_uri_name = 'serial_number'
		filtering = {
			'given_name': ALL,
		}
		fields = [
			'poll_rate',
			'given_name',
			'power_mode',
			'location',
			'is_charging',
			'battery_life',
			'temperature',
			'operating_current',
			'signal_strength',
			'gps_activated',
			'gps_satellite_count',
			'last_request',
		]