import datetime
import logging

from django.db.models import F, DecimalField
from django.db.models.functions import Radians, Sin, Power, Cos, ATan2, Sqrt
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from account.api.serializers import UserProfileSerializer
from account.models import User
from core.Response import Response

logger = logging.getLogger('accounts')


class AroundUserView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    logger = logger

    def get(self, request, *args, **kwargs):
        lat = request.query_params.get('lat')
        lng = request.query_params.get('lng')
        max_range = request.query_params.get('max_range')
        limit_time = request.query_params.get('limit_time')
        gender = request.query_params.get('gender', 'a')
        time_format = "%d %H:%M"
        try:
            lat, lng, max_range = float(lat), float(lng), float(max_range)
        except:
            return Response(message='check input values', dev_message='lat long max_range must be decimal',
                            status=400)
        dlat = Radians(F('lat') - lat, output_field=DecimalField())
        dlong = Radians(F('lng') - lng, output_field=DecimalField())

        a = (Power(Sin(dlat / 2), 2) + Cos(Radians(lat, output_field=DecimalField()))
             * Cos(Radians(F('lat'), output_field=DecimalField())) * Power(Sin(dlong / 2), 2)
             )

        c = 2 * ATan2(Sqrt(a), Sqrt(1 - a))
        d = 6371 * c
        users = User.objects.annotate(distance=d).filter(distance__lte=max_range)
        if gender != 'a':
            users = users.filter(gender=gender)
        if limit_time:
            try:
                now = datetime.datetime.now()
                limit_time = datetime.datetime.strptime(limit_time, time_format).replace(year=now.year, month=now.month)
                limit_time = now.replace(day=now.day - limit_time.day, hour=now.hour - limit_time.hour,
                                         minute=now.minute - limit_time.minute)
            except ValueError:
                return Response(message='invalid date', dev_message='format like %d %H:%M', status=400)
            users = users.filter(location_time__gte=limit_time)
        return Response(UserProfileSerializer(users, many=True).data, status=200)
