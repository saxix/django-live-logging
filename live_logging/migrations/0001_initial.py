# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import live_logging.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LogAggregate',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('filename', models.CharField(null=True, max_length=50, blank=True)),
                ('function_name', models.CharField(null=True, max_length=50, blank=True)),
                ('level', models.PositiveIntegerField(choices=[(20, b'Info'), (30, b'Warning'), (10, b'Debug'), (40, b'Error'), (50, b'Critical')], default=50, db_index=True)),
                ('line_number', models.PositiveIntegerField(default=0)),
                ('module', models.CharField(null=True, max_length=50, blank=True)),
                ('msg', models.TextField(null=True, blank=True)),
                ('name', models.CharField(max_length=200, default=b'root', db_index=True)),
                ('path', models.CharField(null=True, max_length=200, blank=True)),
                ('times_seen', models.PositiveIntegerField(default=1)),
                ('last_seen', models.DateTimeField(auto_now=True)),
                ('first_seen', models.DateTimeField(auto_now_add=True)),
                ('checksum', models.CharField(unique=True, max_length=32)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LogEntry',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('filename', models.CharField(null=True, max_length=50, blank=True)),
                ('function_name', models.CharField(null=True, max_length=50, blank=True)),
                ('level', models.PositiveIntegerField(choices=[(20, b'Info'), (30, b'Warning'), (10, b'Debug'), (40, b'Error'), (50, b'Critical')], default=50, db_index=True)),
                ('line_number', models.PositiveIntegerField(default=0)),
                ('module', models.CharField(null=True, max_length=50, blank=True)),
                ('msg', models.TextField(null=True, blank=True)),
                ('name', models.CharField(max_length=200, default=b'root', db_index=True)),
                ('path', models.CharField(null=True, max_length=200, blank=True)),
                ('args', live_logging.fields.TupleField(null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('exc_text', models.TextField(null=True, blank=True)),
                ('process', models.PositiveIntegerField(default=0)),
                ('process_name', models.CharField(null=True, max_length=200, blank=True)),
                ('thread', models.DecimalField(decimal_places=0, max_digits=21)),
                ('thread_name', models.CharField(null=True, max_length=200, blank=True)),
                ('extra', live_logging.fields.JSONField(blank=True)),
                ('log_aggregate', models.ForeignKey(null=True, to='live_logging.LogAggregate', blank=True)),
            ],
            options={
                'verbose_name_plural': 'Log entries',
            },
            bases=(models.Model,),
        ),
    ]
