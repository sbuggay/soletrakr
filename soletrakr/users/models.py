from django.db import models
from django.contrib.auth.models import User, check_password
from django.contrib.contenttypes.models import ContentType
from django.contrib.localflavor.us import models as us_models

from tastypie.models import create_api_key

try:
    models.signals.post_save.connect(create_api_key, sender=User) # link user creation to API key creation
except Exception, e:
    pass



class Profile(models.Model):
	"""
	User profile to hold metadata about
	user for app functionality and distinguishing
	between customer and staff users.
	"""
	user = models.OneToOneField(User, related_name='profile')
	phone_number = us_models.PhoneNumberField(blank=True)
	is_staff = models.BooleanField(default=False)


	def __unicode__(self):
		return self.user.email


	def set_phone_number(self, number):
		"""
		Function used to set the phone number of
		the given profile.

		@param number: 		New form-validated phone number
		"""
		self.phone_number = number
		self.save()


class UserManager(models.Manager):
	"""
	Manager class to handle common tasks by Users.
	"""

	@classmethod
	def create_user(self, email, password):
		"""
		Function used to create new users.
		"""
		new_user = User.objects.create (
			username = email,
			email = email
		)
		new_user.set_password(password)
		new_user.save()

		new_profile = Profile.objects.create (
			user = new_user
		)
		new_profile.save()

		return new_user


	@classmethod
	def set_staff_user(self, user):
		"""
		Function used to set a previously created user
		object to staff.
		"""
		user.profile.is_staff = True
		user.profile.save()

		return user


	@classmethod
	def create_staff_user(self, email, password):
		"""
		Function used to create new staff users.
		"""
		new_user = self.create_user(email, password)
		self.set_staff_user(new_user)

		return new_user
