from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

AUTH_USER_MODEL = "account.User"
ROOT_URLCONF = "infrastructure.urls"
WSGI_APPLICATION = "infrastructure.wsgi.application"

MEDIA_URL = "/media/"
MEDIA_ROOT = Path.joinpath(BASE_DIR, "media")
STATIC_URL = "/static/"
STATIC_ROOT = Path.joinpath(BASE_DIR, "static")
