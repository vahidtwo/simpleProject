# Create your models here.

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
# Create your models here.
from rest_framework_simplejwt.tokens import RefreshToken

from core.models import AbstractBaseModel
from core.randomize_file import RandomFileName


class UserManager(BaseUserManager):

    def create_user(self, username, email, first_name, last_name, password=None, **kwargs):
        if email is None:
            raise TypeError('Users should have a Email')

        user = self.model(username=username, first_name=first_name, last_name=last_name,
                          email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user('admin', email, 'admin', 'admin', password, age=10)
        user.is_superuser = True
        user.is_staff = True
        user.is_verified = True
        user.save()
        return user


class UserGender(models.TextChoices):
    FEMALE = 'f'
    MALE = 'm'


class User(AbstractBaseUser, PermissionsMixin, AbstractBaseModel):
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    username = models.CharField(max_length=255, unique=True, db_index=True)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)

    lat = models.DecimalField(max_digits=23, decimal_places=20, null=True)
    lng = models.DecimalField(max_digits=24, decimal_places=20, null=True)

    location_time = models.DateTimeField(auto_now=True)

    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    image = models.ImageField(upload_to=RandomFileName('user'), null=True)
    gender = models.CharField(max_length=1, choices=UserGender.choices, default=UserGender.MALE)
    age = models.IntegerField()

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
