.. image:: https://travis-ci.org/shulcsm/django-enumeration.svg?branch=master
    :target: https://travis-ci.org/shulcsm/django-enumeration

===========
Django enumeration sequences
===========

**Consistent, gapless, periodic(optional) sequences with number formatting for accounting documents and such**


Requirements
==============

* Postgres 9.5+
* Python 3.6+



Installation
____________

1. pip install django-enumeration

2. Add "enumeration" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'enumeration',
    ]

3. Run `python manage.py migrate` to create the enumeration models.

