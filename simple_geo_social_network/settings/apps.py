INSTALLED_APPS_DJANGO = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

INSTALLED_APPS = [
    'account',
    'corsheaders',
]

INSTALLED_APPS_3RD = [
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
]


INSTALLED_APPS = [
    *INSTALLED_APPS_DJANGO,
    *INSTALLED_APPS,
    *INSTALLED_APPS_3RD,
]
