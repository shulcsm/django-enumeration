============================
Django enumeration sequences
============================

**Consistent, gapless, periodic(optional) sequences with number formatting for accounting documents and such**


Requirements
==============

* Postgres 9.5+
* Python 3.8+
* Django 4+


Installation
____________

1. pip install django-enumeration

2. Add "enumeration" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'enumeration',
    ]

3. Run `python manage.py migrate` to create the enumeration models.



Development
____________

DJANGO_SETTINGS_MODULE=enumeration.tests.settings django-admin makemigrations