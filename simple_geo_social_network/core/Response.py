from rest_framework.response import Response

from core import dictionary


class Response(Response):
    def __init__(self, data=None, message=None, dev_message=None, status=None, exception=None, headers=None,
                 paginate=None, extra=None):
        if exception:
            super().__init__(
                {"data": data, "detail": dictionary.invalid_serializer_msg, 'dev_message': exception, 'extra': extra},
                status=400, headers=headers)
        else:
            super().__init__(
                {"data": data, "detail": message, "dev_message": dev_message, "paginate": paginate, 'extra': extra},
                status=status, headers=headers)
