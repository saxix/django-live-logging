# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('live_logging', '0003_initial_data'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='formatter',
            options={'ordering': (b'name',)},
        ),
        migrations.AlterModelOptions(
            name='handler',
            options={'ordering': (b'name',)},
        ),
        migrations.AlterModelOptions(
            name='logger',
            options={'ordering': (b'name',)},
        ),
        migrations.RemoveField(
            model_name='logentry',
            name='log_aggregate',
        ),
        migrations.DeleteModel(
            name='LogAggregate',
        ),
        migrations.AlterField(
            model_name='formatter',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='handler',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='logger',
            name='name',
            field=models.CharField(blank=True, max_length=100, unique=True),
        ),
    ]
