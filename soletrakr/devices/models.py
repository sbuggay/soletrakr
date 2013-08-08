import datetime
import json
import requests

from django.core import validators
from django.core.urlresolvers import reverse
from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver

from django_localflavor_us import models as us_models
from south.modelsinspector import add_introspection_rules

# add introspection rule for custom model field for south DB migrations
add_introspection_rules([], ["^django_localflavor_us\.models\.PhoneNumberField"])


class DeviceError(Exception):
	"""
	Custom exception class used to represent errors
	and exceptions dealing with devices.
	"""
	def __init__(self, message):
		self.message = message


class Device(models.Model):
	"""
	Represents a SoleTrakr tracking device.
	"""
	POWER_MODES = ( # Power mode choices for device
		('PM01', 'Power mode 1'),
		('PM02', 'Power mode 2'),
		('PM03', 'Power mode 3'),
		('PM04', 'Power mode 4'),
		('PM05', 'Power mode 5'),
		('PM06', 'Power mode 6'),
		('PM07', 'Power mode 7'),
		('PM08', 'Power mode 8'),
		('PM09', 'Power mode 9'),
		('PM10', 'Power mode 10'),
	)

	# User-inputted data
	given_name = models.CharField(max_length=50, blank=True, null=True) # familiar name of device for user
	poll_rate = models.IntegerField(validators=[validators.MinValueValidator(2)], default=60) # in seconds

	# Relational fields
	user = models.ForeignKey(User, related_name='devices', blank=True, null=True)

	# Device info
	serial_number = models.IntegerField(unique=True) # how many digits?
	sim_serial_number = models.IntegerField(unique=True) # how many digits?
	date_manufactured = models.DateField()
	date_activated = models.DateField(blank=True, null=True)
	phone_number = us_models.PhoneNumberField(blank=True)

	# Spatial data
	location = models.PointField(blank=True, null=True)
	objects = models.GeoManager()

	# Polled info
	battery_life = models.IntegerField(validators=[
		validators.MinValueValidator(0), validators.MaxValueValidator(100)], blank=True, null=True) # percentage
	is_charging = models.NullBooleanField()
	temperature = models.FloatField(blank=True, null=True) # in C
	operating_current = models.FloatField(blank=True, null=True) # in mA
	power_mode = models.CharField(choices=POWER_MODES, max_length=4, blank=True, null=True)
	signal_strength = models.FloatField(blank=True, null=True) # in dB

	gps_activated = models.BooleanField(default=False)
	gps_satellite_count = models.IntegerField(validators=[validators.MinValueValidator(0)], blank=True, null=True)
	last_request = models.DateTimeField(blank=True, null=True)

	# Meta fields
	is_active = models.BooleanField(default=False)


	def __unicode__(self):
		"""
		Unicode representation of device for use on admin site.
		"""
		if self.is_active:
			if self.given_name:
				return '%s' % self.given_name
			else:
				return 'Activated: #%s' % self.serial_number
		else:
			return 'Unactivated: #%s' % self.serial_number


	def _activation_check(self):
		"""
		Helper function used within API calls to make sure 
		the given device is active before trying to make calls
		to its resources on the API.

		@raise 	ValueError: 	if device is not active
		"""
		if not self.is_active:
			raise DeviceError('Device is not active.')


	def _get_resource_url(self):
		"""
		Helper function used to determine the given
		device's resource url for REST API calls.
	
		@raise DeviceError: 	if device is not active
		@return: 				resource url as string
		"""
		self._activation_check()
		#domain = 'Site.objects.get(pk=1).domain'
		domain = 'localhost:8000'
		uri = reverse('api_dispatch_detail', kwargs={
			'resource_name' : 'devices',
			'serial_number': str(self.serial_number)
		})
		email = self.user.email
		api_key = self.user.api_key.key

		return str('http://%s%s?format=json&username=%s&api_key=%s' % (domain, uri, email, api_key))


	def _api_get(self):
		"""
		Helper function perform HTTP GET and return
		the JSON response data at the device's API URI.

		@raise DeviceError: 	if device is not active
		@raise HTTPError: 		if 400 response code from server at specified url
		@return: 				JSON data at specified url
		"""
		self._activation_check()
		r = requests.get(self._get_resource_url())
		r.raise_for_status() # raise Exception if 400 error from server

		return r.json()


	def _api_patch(self, payload):
		"""
		Helper function to perform HTTP PATCH of JSON data
		at the devices' API URI.
		
		@param payload: 		the JSON update data
		@raise DeviceError: 	if device is not active
		@raise HTTPError: 		if 400 response code from server at specified url
		"""
		self._activation_check()
		headers = {'content-type': 'application/json'}
		r = requests.patch(self._get_resource_url(), headers=headers, data=json.dumps(payload))
		r.raise_for_status() # raise Exception if 400 error from server


	def set_user(self, user):
		"""
		Set the user of the device.

		@param user: 		user object
		@raise TypeError: 	if parameter user is not of object type User
		"""
		if not isinstance(user, User):
			raise TypeError('parameter \'user\' must be of type User')
		else:
			self.user = user
			self.save()


	def set_update_rate(self, rate):
		"""
		Set the update rate of the device.

		@param rate: 			rate as integer
		@raise DeviceError: 	if device is not active
		@raise TypeError: 		if parameter rate is not of type integer
		@raise ValueError: 		if rate is smaller than 2 (maximum poll rate)
		@raise HTTPError: 		if 400 response code from server at specified url
		"""
		if not isinstance(rate, int):
			raise TypeError('parameter \'rate\' must be of type integer')
		if rate < 2:
			raise ValueError('minimum rate value is 2')
		else:
			self._api_patch({'poll_rate' : rate})


	def set_given_name(self, name):
		"""
		Sets the given name of the device through API.

		@param name: 			user given name
		@raise DeviceError: 	if device is not active
		@raise TypeError: 		if name parameter is not of type string
		@raise HTTPError: 		if 400 response code from server at specified url
		"""
		if not isinstance(name, str):
			raise TypeError('parameter \'name\' must be of type string')
		else:
			self._api_patch({'given_name' : name})


	def activate(self, user):
		"""
		Activates a device on the sytem and ties
		the device to a given user object.

		@param user: 		user object
		"""
		try:
			self.set_user(user)
			self.set_update_mode('BRW')
			self.date_activated = datetime.date.today()
			self.is_active = True
			self.save()
			return True

		except:
			return False
	

	def reset(self):
		"""
		Resets the device.
		"""
		pass


	def shutdown(self):
		"""
		Shuts down the device.
		"""
		pass


class DeviceManager(models.GeoManager):
	"""
	Manager class to handle common tasks related
	to devices.
	"""
	@classmethod
	def create_device(self, serial_number, sim_serial_number, date_manufactured, phone_number):
		"""
		Function used to create a new, unactivated device in the SoleTrakr
		database. Once a device has been created, it must be activated to be
		attached to a customer.

		@param serial_number:			serial number of the device
		@param sim_serial_number: 		serial number of the device's sim card
		@param date_manufactured: 		date the device was manufactured
		@param phone_number: 			phone number of device for SMS ?
		@return: 						the newly created device object
		"""
		new_device = Device.objects.create (
			serial_number = serial_number,
			sim_serial_number = sim_serial_number,
			date_manufactured = date_manufactured,
			phone_number = phone_number
		)
		new_device.save()

		return new_device


	@classmethod
	def activate_device(self, device, user):
		"""
		Function used to activate previously created devices by attaching them
		to users and exposing them on the REST API to begin polling the device.

		@param device: 					the device object to be activated
		@return: 						true if the device activated successfully, false otherwise
		"""
		return device.activate(user)