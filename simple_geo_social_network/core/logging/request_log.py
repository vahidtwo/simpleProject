from core.logging import base_log


def request_log(path, request, *args, **kwargs):
    version = kwargs.pop('version', None)
    args = ' args={}'.format(args) if args else ''
    kwargs = ' kwargs={}'.format(kwargs) if kwargs else ''
    qp = ' qp={}'.format(dict(request.query_params)) if request.query_params else ''
    data = ' data={}'.format(request.data) if request.data else ''
    return '{}{}{}{}{}'.format(base_log(path, version, request), args, kwargs, qp, data)
