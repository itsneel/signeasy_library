"""Library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
#!/usr/bin/python

import re
import sys
from Crypto import Random

from allauth.account import views as allauth_views

from django.conf import settings
from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.generic import RedirectView

from djrill import DjrillAdminSite
from tastypie.api import NamespacedApi

# Api Resources
from books.api import BooksResource
from members.api import MembersResource

# Signals
from members import signals

admin.site = DjrillAdminSite()
admin.autodiscover()

v1_api = NamespacedApi(api_name='v1', urlconf_namespace='namespace')
v1_api.register(BooksResource())
v1_api.register(MembersResource())

urlpatterns = patterns(
    '',
    # admin urls
    url(r'^lib/admin/', include(admin.site.urls)),
    url(r'^lib/admin/doc/', include('django.contrib.admindocs.urls')),
    # api v1 urls
    url(r'^api/', include(v1_api.urls)),
)

Random.atfork()

if settings.DEBUG or 'test' in sys.argv:
    static_url = re.escape(settings.STATIC_URL.lstrip('/'))
    urlpatterns += patterns('',
        url(r'^%s(?P<path>.*)$' % static_url, 'django.views.static.serve', {
                'document_root': settings.STATIC_ROOT,
        }),
    )
