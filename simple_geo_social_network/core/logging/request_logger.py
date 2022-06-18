from functools import wraps

from core.logging import request_log, log_data


def request_logger(logger=None, version=None):
    def decorator(function):
        @wraps(function)
        def wrapper(view_class, request, *args, **kwargs):
            nonlocal logger, version

            path, _logger, _version = log_data(view_class)
            if not logger:
                logger = _logger
            if not version:
                version = _version

            if logger:
                logger.info(request_log(path, request, version=version, *args, **kwargs))
            return function(view_class, request, *args, **kwargs)

        return wrapper

    return decorator
