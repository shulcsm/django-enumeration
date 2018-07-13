DATABASE_ENGINE = 'sqlite3'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'enumeration_test',
        'USER': 'postgres'
    }
}


INSTALLED_APPS = [
    # 'django.contrib.contenttypes',
    # 'django.contrib.sites',
    # 'django.contrib.auth',
    # 'django.contrib.admin',

    'enumeration',
]

SECRET_KEY = 'enumeration'
