Django Live Logging
===================

Allow live editing of logging configuration in django projects and/or log to internal database table.


This project does not pretend to be 'state of the art',
was written in few hours to help to troubleshoot applications where is not possible to access to log file easily.
It allow you to temporarly enable database logging and change/add logging level and loggers using django admin interface.

Thanks to Joeri Bekker for the https://github.com/joeribekker/django-logdb application
from which the database logging part of this package was taken.


.. note:: Only tested on Django 1.7


Quick Installation
------------------

::

   pip install django-live-logging


Once installed, update your Django `settings.py` and add ``live_logging`` to your
INSTALLED_APPS::

    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        ...
        'live_logging',
    )


Configure Database logging
--------------------------
Create an handler in your logging configuration to store into database.
::

    LOGGING = {
        ...
         'handlers': {
            ...
            'db': {
                'level': 'DEBUG',
                'class': 'live_logging.handlers.DjangoDatabaseHandler',
                },
          }
        }
