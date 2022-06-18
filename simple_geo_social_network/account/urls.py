from django.urls import path

from account.api.v1 import RegisterView, LoginAPIView, VerifyEmail, RequestPasswordResetEmail, \
    PasswordTokenCheckAPI, SetNewPasswordAPIView, ProfileUserView
from account.api.v1.get_arrount_user import AroundUserView
from account.api.v1.update_location import UpdateLocationUser

urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('profile/', ProfileUserView.as_view(), name="user-profile"),
    path('login/', LoginAPIView.as_view(), name="login"),
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
    path('reset-password/', RequestPasswordResetEmail.as_view(),
         name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/',
         PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete/', SetNewPasswordAPIView.as_view(),
         name='password-reset-complete'),

    path('around-user/', AroundUserView.as_view(), name="around-user"),
    path('update-location/', UpdateLocationUser.as_view(), name="update-location"),
]
