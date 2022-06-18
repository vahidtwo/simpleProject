from rest_framework import serializers

from account.models import User
from core.serializers import ModelSerializer


class RegisterSerializer(ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    age = serializers.IntegerField(required=True, min_value=10, max_value=100)

    class Meta:
        model = User
        fields = ['email','username', 'password', 'first_name', 'last_name', 'lat', 'lng', 'image', 'age', 'gender']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
