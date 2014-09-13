# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import live_logging.fields


class Migration(migrations.Migration):

    dependencies = [
        ('live_logging', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Formatter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=100)),
                ('format', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Handler',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=100)),
                ('level', live_logging.fields.LogLevelField(choices=[(50, b'CRITICAL'), (40, b'ERROR'), (30, b'WARNING'), (20, b'INFO'), (10, b'DEBUG'), (0, b'NOTSET')], help_text=b'')),
                ('handler', models.CharField(max_length=255)),
                ('formatter', models.ForeignKey(to='live_logging.Formatter')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Logger',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=100)),
                ('propagate', models.BooleanField(default=False)),
                ('level', live_logging.fields.LogLevelField(choices=[(50, b'CRITICAL'), (40, b'ERROR'), (30, b'WARNING'), (20, b'INFO'), (10, b'DEBUG'), (0, b'NOTSET')], help_text=b'')),
                ('handlers', models.ManyToManyField(to='live_logging.Handler')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
