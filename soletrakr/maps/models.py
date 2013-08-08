import datetime
import json
import requests

from django.core import validators
from django.core.urlresolvers import reverse
from django.contrib.gis.db import models
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.dispatch import receiver


class Path(models.Model):
	"""
	Object to represent a device's path history.
	"""
	# relational fields
	device = models.OneToOneField('devices.Device', related_name='path')

	# Spatial data
	points = models.LineStringField(blank=True)
	objects = models.GeoManager()


class Geofence(models.Model):
	# relational fields
	device = models.OneToOneField('devices.Device', related_name='geofence')

	# spatial data
	area = models.PolygonField(blank=True, null=True)
	objects = models.GeoManager()