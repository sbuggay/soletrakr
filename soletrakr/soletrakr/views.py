""" Python Package Imports """
# n/a

""" Django Package Imports """
from django.shortcuts import render
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

""" Internal imports """
from users.forms import ChangePasswordForm

def test(request):
	context = dict()
	return render(request, 'base.html', context)

def faq(request):
	context = dict()
	return render(request, 'faq.html', context)

def api_documentation(request):
	context = dict()
	return render(request, 'api.html', context)

def contact_us(request):
	context = dict()
	return render(request, 'contact_us.html', context)

def about_us(request):
	context = dict()
	return render(request, 'about_us.html', context)

def prototype(request):
	context = dict()
	return render(request, 'prototype.html', context)