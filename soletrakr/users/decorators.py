from django.contrib.auth.decorators import user_passes_test


def staff_required(function=None):
	"""
	Decorator for view functions to enforce staff
	permisisons on certain pages.
	"""
	actual_decorator = user_passes_test (
		lambda u: u.profile.is_staff,
		login_url='/dashboard/'
	)
	if function:
		return actual_decorator(function)

	return actual_decorator