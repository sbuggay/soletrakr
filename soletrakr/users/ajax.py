from django.contrib.auth import logout

from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax


@dajaxice_register
def logout_user(request):
	"""
	AJAX endpoint function which is used to log a user out.

	@param request: 		user's XMLHttpRequest
	"""
	dajax = Dajax()

	if request.user.is_authenticated():
		logout(request)
		dajax.redirect('/', delay=10) # 10ms delay on redirect

	else:
		dajax.redirect('/login/', delay=10)

	return dajax.json()


@dajaxice_register
def set_user(request):
	"""
	AJAX view which is used to set the user context 
	for API access.
	"""
	dajax = Dajax()

	if request.user.is_authenticated():
		if request.user.email and request.user.api_key:
			dajax.script('var username =\"%s\";' % request.user.email)
			dajax.script('var api_key =\"%s\";' % request.user.api_key.key)

	return dajax.json()