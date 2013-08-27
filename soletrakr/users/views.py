from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth import login as auth_login, authenticate

from userprofiles.auth_backends import EmailOrUsernameModelBackend

from users.forms import *


@csrf_protect
def login(request):
	"""
	View for login page.
	"""
	if request.method == 'POST':
		login_form = LoginForm(request.POST)

		if login_form.is_valid():
			login_form.save(request)
			return HttpResponseRedirect('/dashboard/')

	else:
		login_form = LoginForm()

	context = {
		'login_form' : login_form,
	}
	return render(request, 'login.html', context)


@csrf_protect
def register(request):
	"""
	View for registration page.
	"""
	if request.method == 'POST':
		register_form = RegisterForm(request.POST)

		if register_form.is_valid():
			register_form.save()
			return HttpResponseRedirect('/login/')
	else:
		register_form = RegisterForm()

	context = {
		'register_form' : register_form,
	}
	return render(request, 'register.html', context)


@csrf_protect
@login_required
def dashboard(request):
	"""
	View for logged-in user's dashboard page, 
	which contains the map and controls.
	"""
	context = {
		# 'user' : request.user,
		# 'devices' : request.user.devices.all(),
	}
	return render(request, 'dashboard.html', context)


@csrf_protect
@login_required
def settings(request):
	"""
	View for the user settings page.
	"""
	if request.method == 'POST':
		print request.POST
		change_password_form = ChangePasswordForm(request.POST)

		if change_password_form.is_valid():
			status = change_password_form.save(user=request.user)
			print status

	else:
		change_password_form = ChangePasswordForm()

	context = {
		'user' : request.user,
		'devices' : request.user.devices.all(),
		'change_password_form' : change_password_form,
	}
	return render(request, 'settings.html', context)