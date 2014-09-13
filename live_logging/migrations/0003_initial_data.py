# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from django.db import models, migrations


def initial_data(apps, schema_editor):
    Formatter = apps.get_model('live_logging.Formatter')
    Formatter.objects.get_or_create(name='full',
                                    defaults={
                                    'format': '%(levelname)-8s: %(asctime)s %(module)s %(process)d %(thread)d %(message)s'})
    Formatter.objects.get_or_create(name='verbose',
                                    defaults={'format': '%(levelname)-8s: %(asctime)s %(name)20s %(message)s'})
    fmt, __= Formatter.objects.get_or_create(name='simple',
                                    defaults={
                                    'format': '%(levelname)-8s: %(asctime)s %(name)20s: %(funcName)s %(message)s'})

    Handler = apps.get_model('live_logging.Handler')
    Handler.objects.get_or_create(name='null',
                                    defaults={
                                    'level': logging.DEBUG,
                                    'formatter': fmt,
                                    'handler': 'django.utils.log.NullHandler'})

    Handler.objects.get_or_create(name='db',
                                    defaults={
                                    'level': logging.DEBUG,
                                    'formatter': fmt,
                                    'handler': 'live_logging.handlers.DjangoDatabaseHandler'})


class Migration(migrations.Migration):
    dependencies = [
        ('live_logging', '0002_formatter_handler_logger'),
    ]

    operations = [
        migrations.RunPython(initial_data),
    ]
