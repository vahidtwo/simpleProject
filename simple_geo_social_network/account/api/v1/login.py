import logging

from rest_framework import generics, status

from account.api.serializers import LoginSerializer
from core.Response import Response

logger = logging.getLogger('accounts')


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    logger = logger

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
