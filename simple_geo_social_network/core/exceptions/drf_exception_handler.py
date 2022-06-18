from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import Http404
from rest_framework import exceptions
from rest_framework.views import set_rollback

from core.logging import exception_log, log_data
from .exception_data import exception_data
from .. import dictionary
from ..Response import Response


def drf_exception_handler(exc, context):
    path, logger, version = log_data(context['view'])
    response, data = exception_data(context['view'])
    if isinstance(exc, IntegrityError):
        exc = exceptions.ValidationError(exc, code=400)
    if isinstance(exc, ValidationError):
        exc = exceptions.ValidationError(exc.messages, code=exc.code)
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()
    api_exception = isinstance(exc, exceptions.APIException)
    if api_exception:
        set_rollback()
        if isinstance(exc.detail, (list, dict)):
            if isinstance(exc.detail, dict):
                keys = exc.detail.keys()
                for key in keys:
                    for err in exc.detail[key]:
                        if hasattr(err, 'code') and err.code == 'unique':
                            response.update({'message': dictionary.unique_msg, 'status': exc.status_code})
                        elif hasattr(err, 'code') and err.code == 'invalid':
                            response.update({'message': err, 'status': exc.status_code})
            else:
                response.update({'message': exc.detail[0], 'status': exc.status_code})
            response.update({'dev_message': exc.detail, 'status': exc.status_code})
        else:
            response.update({'message': exc.detail, 'status': exc.status_code})

    try:
        if api_exception:
            logger.error(exception_log(path, exc, request=context['request'], version=version, **data))
        else:
            logger.exception(exception_log(path, exc, request=context['request'], version=version, **data))
    except Exception as e:
        pass

    return Response(**response)
