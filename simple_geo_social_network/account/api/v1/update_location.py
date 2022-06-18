import logging

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from core import dictionary
from core.Response import Response

logger = logging.getLogger('accounts')


class UpdateLocationUser(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    logger = logger

    def put(self, request):
        user = request.user
        user.lat = request.data.get('lat')
        user.lng = request.data.get('lng')
        user.save()
        return Response(message=dictionary.update_location_user)