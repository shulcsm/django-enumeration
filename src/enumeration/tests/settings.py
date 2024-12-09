DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "enumeration_test",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "localhost",
    }
}


INSTALLED_APPS = [
    # 'django.contrib.contenttypes',
    # 'django.contrib.sites',
    # 'django.contrib.auth',
    # 'django.contrib.admin',
    "enumeration",
    "enumeration.tests",
]

SECRET_KEY = "enumeration"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

USE_TZ = False
