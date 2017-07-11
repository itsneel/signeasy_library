"""Utils module for API."""

import json
import urllib2
import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils import timezone
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.serializers import Serializer


logger = logging.getLogger(__name__)


class required(object):
    """Annotation for specifying required fields for TastyPie API."""

    def __init__(self, params, get_json_body=True):
        self._params = params
        self._get_json_body = get_json_body

    def _get_req(self, request):
        if request.method in ['POST', 'PUT']:
            try:
                return json.loads(request.body)
            except ValueError, e:
                raise_json_response(status=407)
        else:
            return request.GET

    def __call__(self, func):
        def inner(resource, request, *args, **kwargs):
            req = self._get_req(request)
            missing_params = [fld for fld in self._params if fld not in req]
            if missing_params:
                return resource.error_response(request, {
                        'success': False,
                        'fields': missing_params, 
                        'reason': 'requiredFieldsNotPresent'
                    })
            additional_args = []
            for param in self._params: 
                additional_args.append(req[param])
            if request.method in ['POST', 'PUT'] and self._get_json_body:
                additional_args.append(req)
            args = tuple(additional_args) + args
            return func(resource, request, *args, **kwargs)
        return inner


class JsonResponse(HttpResponse):
    def __init__(self, status, body=None):
        super(JsonResponse, self).__init__(status=status, content_type='application/json')
        if not body:
            body = {}
        self.content = json.dumps(body)


def raise_json_response(status, body=None):
    raise ImmediateHttpResponse(response=JsonResponse(status, body))
