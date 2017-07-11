#!/usr/bin/python

import json

from django.conf import settings
from django.conf.urls import url
from django.http import HttpResponseRedirect

from tastypie import fields
from tastypie import resources
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authentication import MultiAuthentication
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import Authorization
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpNotFound, HttpResponse, HttpUnauthorized
from tastypie.utils.urls import trailing_slash

from books import mod
from library import decorators


class MembersResource(resources.Resource):

    class Meta:
        resource_name = 'members'
        authorization = Authorization()
        authentication = MultiAuthentication(
            SessionAuthentication(), ApiKeyAuthentication())

    def prepend_urls(self):
        return [
            url(r'^(?P<resource_name>{})/'.format(
                self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_all_books'), name='get_all_books'),
            url(r'^(?P<resource_name>{})/(?P<market_place>\w+)/inventory/update'.format(
                self._meta.resource_name, trailing_slash()),
                self.wrap_view('update_inventory'), name='api_update_inventory'),
        ]

    def get_all_books(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        # self.is_authenticated(request)
        is_active = request.GET.get('is_active') or 0
        is_active = bool(int(is_active))
        data = mod.get_all_mp(get_only_active=is_active)
        return self.create_response(request, {'objects': data})
