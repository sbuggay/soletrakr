from django.conf.urls import patterns, url, include


urlpatterns = patterns('users.views',
	# login/registration
	url(r'^login/$', 'login', name='login'),
	url(r'^register/$', 'register', name='register'),

	# user-specific content
	url(r'^dashboard/$', 'dashboard', name='dashboard'),
	url(r'^settings/$', 'settings', name='settings'),

	# User-related API URIs
	#url(r'^api/', include(UserResource().urls)),
)

urlpatterns += patterns('',
	url(r'^password/forgot/$', 
        'django.contrib.auth.views.password_reset', 
        {
        	'post_reset_redirect' : '/password/forgot/sent/',
        	'template_name' : 'forgot_password.html',
        },
        name="forgot_password"),

    url(r'^password/forgot/sent/$',
        'django.contrib.auth.views.password_reset_done',
        name='password_reset_sent'),

    url(r'^password/forgot/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 
        'django.contrib.auth.views.password_reset_confirm', 
        {'post_reset_redirect' : 'password/forgot/done/'},
        name='password_reset'),

    url(r'^password/forgot/done/$', 
        'django.contrib.auth.views.password_reset_complete',
    	name='password_reset_complete'),
)