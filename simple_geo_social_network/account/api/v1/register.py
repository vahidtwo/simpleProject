import logging

import jwt
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework import generics, status

from account.api.serializers import RegisterSerializer
from account.models import User
from account.utils import Util
from core.Response import Response

logger = logging.getLogger('accounts')


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    logger = logger

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        token = jwt.encode({'username': user.email}, settings.SECRET_KEY)
        current_site = get_current_site(request).domain
        relative_link = reverse('email-verify')
        abs_url = 'http://' + current_site + relative_link + "?token=" + str(token)
        email_body = 'Hi ' + user.first_name + ' Use the link below to verify your email \n' + abs_url
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email'}

        Util.send_email(data)
        return Response(status=status.HTTP_201_CREATED)
