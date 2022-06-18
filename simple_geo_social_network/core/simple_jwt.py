from rest_framework_simplejwt.authentication import JWTAuthentication as _JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from rest_framework_simplejwt.settings import api_settings

from core import dictionary


class JWTAuthentication(_JWTAuthentication):
    def get_user(self, validated_token):
        """
        Attempts to find and return a user using the given validated token.
        """
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
        except KeyError:
            raise InvalidToken('Token contained no recognizable user identification')

        try:
            user = self.user_model.objects.get(**{api_settings.USER_ID_FIELD: user_id})
        except self.user_model.DoesNotExist:
            raise AuthenticationFailed(dictionary.user_not_found, code='user_not_found')
        if not user.is_active:
            raise AuthenticationFailed(dictionary.user_not_active, code='user_in_active')

        return user
