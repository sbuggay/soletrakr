from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
admin.autodiscover()

from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()

urlpatterns = patterns('',
    # Main urls
    url(r'^$', 'soletrakr.views.test', name='base'),
    url(r'^faq/$', 'soletrakr.views.faq', name='faq'),
    url(r'^doc/$', 'soletrakr.views.api_documentation', name='api'),
    url(r'^contact_us/$', 'soletrakr.views.contact_us', name='contact_us'),
    url(r'^about_us/$', 'soletrakr.views.about_us', name='about_us'),
    url(r'^prototype/$', 'soletrakr.views.prototype', name='prototype'),

    # User-related urls
    url(r'^', include('users.urls')),
    # Device-related urls
    url(r'^', include('devices.urls')),
    # Maps-related urls
    url(r'^', include('maps.urls')),

    # Other urls
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
)
urlpatterns += staticfiles_urlpatterns() # static site
