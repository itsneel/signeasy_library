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

from books import exceptions
from books import mod
from members import exceptions as common_exceptions
from library import decorators


class BooksResource(resources.Resource):

    class Meta:
        resource_name = 'books'
        authorization = Authorization()
        authentication = MultiAuthentication(
            SessionAuthentication(), ApiKeyAuthentication())

    def prepend_urls(self):
        return [
            url(r'^(?P<resource_name>{})/'.format(
                self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_all_books'), name='get_all_books'),
            url(r'^(?P<resource_name>{})/add'.format(
                self._meta.resource_name, trailing_slash()),
                self.wrap_view('add_book'), name='api_add_book'),
            url(r'^(?P<resource_name>{})/issue'.format(
                self._meta.resource_name, trailing_slash()),
                self.wrap_view('issue_book'), name='api_issue_book'),
        ]

    def get_all_books(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        # self.is_authenticated(request)
        data = mod.get_all_books()
        return self.create_response(request, {'objects': data})

    @decorators.required(params=['sku'])
    def add_book(self, request, sku, **kwargs):
        self.method_check(request, allowed=['post', 'put'])
        # self.is_authenticated(request)
        data = json.loads(request.body)
        try:
            book, created = mod.add_or_update_book(sku, data=data)
        except (exceptions.SkuNotpresetError, common_exceptions.RaceConditionIntegrityError) as e:
            error = e.get_error_response()
            return self.error_response(request, error)
        return self.create_response(request, {
            'created': created,
            'book': book.__dict__
        })

    @decorators.required(params=['member_id', 'book_sku'])
    def issue_book(self, request, member_id, book_sku, **kwargs):
        self.method_check(request, allowed=['post'])
        # self.is_authenticated(request)
        try:
            issue = mod.issue_book(member_id, book_sku)
        except () as e:
            error = e.get_error_response()
            return self.error_response(request, error)
        
        return self.create_response(request, {'status': issue})

