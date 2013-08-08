from django.contrib import admin

from users.models import Profile


class ProfileAdmin(admin.ModelAdmin):
	"""
	Register devices on Django admin site.
	"""
	pass

admin.site.register(Profile, ProfileAdmin)