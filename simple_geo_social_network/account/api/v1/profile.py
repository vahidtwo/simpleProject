import logging

from rest_framework.generics import GenericAPIView

from account.api.serializers import UserProfileSerializer
from rest_framework.permissions import IsAuthenticated

from core.Response import Response

logger = logging.getLogger('accounts')


class ProfileUserView(GenericAPIView):
    logger = logger
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializer

    def get(self, request):
        user = request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data)
