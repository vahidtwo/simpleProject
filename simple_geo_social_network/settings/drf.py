import datetime

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'core.exceptions.drf_exception_handler',
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework_simplejwt.authentication.JWTAuthentication",),
}
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": datetime.timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": datetime.timedelta(days=365),
}
