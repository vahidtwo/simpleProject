from rest_framework import serializers

from account.models import User
from core.serializers import ModelSerializer


class EmailVerificationSerializer(ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']
