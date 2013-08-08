from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from devices.forms import DeviceCreationForm, DeviceActivationForm
from users.decorators import staff_required


@csrf_protect
@staff_required
@login_required
def create_device(request):
	"""
	View for device creation page.
	"""
	if request.method == 'POST':
		form = DeviceCreationForm(request.POST)

		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/dashboard/')

	else:
		form = DeviceCreationForm()

	context = {
		'form' : form,
	}
	return render(request, 'create_device.html', context)


@csrf_protect
@staff_required
@login_required
def activate_device(request):
	"""
	View for device activation page.
	"""
	if request.method == 'POST':
		form = DeviceActivationForm(request.POST)

		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/dashboard/')

	else:
		form = DeviceActivationForm()

	context = {
		'form' : form,
	}
	return render(request, 'activate_device.html', context)