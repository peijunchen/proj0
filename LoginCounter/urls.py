from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'my_warmup.views.home', name='home'),
    # url(r'^my_warmup/', include('my_warmup.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
	url(r'^client.html$','warmup.views.index'),
	#url(r'^admin/',include(admin.site.urls)),
	url('','warmup.views.index'),
	url(r'^TESTAPI/resetFixture/','warmup.views.index')
)
