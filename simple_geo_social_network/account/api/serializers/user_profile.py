from account.models import User
from core.serializers import ModelSerializer


class UserSerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = User


class UserProfileSerializer(ModelSerializer):

    class Meta:
        exclude = ('password', 'groups', 'user_permissions', 'deleted')
        model = User

