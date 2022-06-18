def base_log(path, version=None, request=None, user=None, ip=None, method=None):
    if not user:
        try:
            user = request.user
        except Exception as e:
            user = 'AnonymousUser'
    if not ip:
        try:
            # fixme: getting ip must be proxy aware too, so if must check 'HTTP_X_FORWARDED_FOR' key too.
            ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
        except Exception as e:
            ip = '0.0.0.0'
    if not method:
        try:
            method = request.method
        except Exception as e:
            method = None

    user_data = ' [{}|{}]'.format(user, ip)
    version = '[{}] '.format(version) if version else ''
    method = ' [{}]'.format(method) if method else ''

    return '{}[{}]{}{}'.format(version, path, method, user_data)
