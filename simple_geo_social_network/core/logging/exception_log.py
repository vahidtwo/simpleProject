from core.logging import base_log


def exception_log(path, exception, *args, **kwargs):
    version = kwargs.pop('version', None)
    request = kwargs.pop('request', None)
    log_user = kwargs.pop('log_user', None)
    log_ip = kwargs.pop('log_ip', None)
    args = ' | {}'.format(str(args)) if args else ''
    kwargs = ' | {}'.format(str(kwargs)) if kwargs else ''
    return '{} [EX] {}{}{}'.format(base_log(path, version, request, log_user, log_ip), exception, args, kwargs)
