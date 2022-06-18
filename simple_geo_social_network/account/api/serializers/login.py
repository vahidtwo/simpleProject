from django.contrib import auth
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from account.models import User
from core.serializers import ModelSerializer


class LoginSerializer(ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=1, write_only=True)
    email = serializers.CharField(max_length=68, min_length=1, write_only=True)
    token = serializers.JSONField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'token')

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        try:
            user = User.objects.get(email=email)
            if not user.check_password(password):
                raise AuthenticationFailed('Invalid credentials, try again')
        except User.DoesNotExist:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')

        return {
            'token': user.tokens()
        }
