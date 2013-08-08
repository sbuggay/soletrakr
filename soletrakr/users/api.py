from django.contrib.auth.models import User

from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization, DjangoAuthorization


class UserResource(ModelResource):
	"""
	Resource class to setup URI endpoints for
	users for REST API.

	!! 	Not currently exposed on API.
	"""
	devices = fields.ToManyField('devices.api.DeviceResource', 'devices', full=True, full_detail=True)

	class Meta:
		queryset = User.objects.filter(is_superuser=False)
		#queryset = User.objects.all()
		resource_name = 'users'
		authentication = ApiKeyAuthentication()
		authorization = Authorization()
		fields = [
			'email',
			'devices',
		]