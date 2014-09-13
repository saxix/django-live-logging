import datetime
import logging
import time

from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.db.models.fields import NOT_PROVIDED


def get_timestamp(date_time):
    """
    Create a `timestamp` from a `datetime` object. A `timestamp` is defined
    as the number of milliseconds since January 1, 1970 00:00. This is like
    Javascript or the Unix timestamp times 1000.
    """
    return time.mktime(date_time.timetuple()) * 1000


def get_datetime(timestamp):
    """
    Takes a `timestamp` and returns a `datetime` object.
    """
    return datetime.datetime.fromtimestamp(int(timestamp / 1000))


class JSONField(models.TextField):
    __metaclass__ = models.SubfieldBase

    def to_python(self, value):
        if isinstance(value, basestring) and value:
            try:
                value = json.loads(value)
            except ValueError:
                return None

        return value

    def get_db_prep_save(self, value, connection):
        if value is None:
            return None

        value = json.dumps(value, cls=DjangoJSONEncoder)
        return super(JSONField, self).get_db_prep_save(value, connection=connection)


class TupleField(models.TextField):
    __metaclass__ = models.SubfieldBase

    def to_python(self, value):
        if value is None:
            return None

        if isinstance(value, basestring):
            try:
                value = tuple(json.loads(value))
            except ValueError:
                return None

        return value

    def get_db_prep_save(self, value, connection):
        if value is None:
            return None

        value = json.dumps(value, cls=DjangoJSONEncoder)
        return super(TupleField, self).get_db_prep_save(value, connection=connection)


class LogLevelField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, primary_key=False, max_length=None, unique=False, blank=False,
                 null=False, db_index=False, rel=None, default=NOT_PROVIDED, editable=True, serialize=True,
                 unique_for_date=None, unique_for_month=None, unique_for_year=None, choices=None, help_text='',
                 db_column=None, db_tablespace=None, auto_created=False, validators=[], error_messages=None):
        choices = ((logging.CRITICAL, 'CRITICAL'),
                   (logging.ERROR, 'ERROR'),
                   (logging.WARNING, 'WARNING'),
                   (logging.INFO, 'INFO'),
                   (logging.DEBUG, 'DEBUG'),
                   (logging.NOTSET, 'NOTSET'),)
        super(LogLevelField, self).__init__(verbose_name, name, primary_key, max_length, unique, blank, null, db_index,
                                            rel, default, editable, serialize, unique_for_date, unique_for_month,
                                            unique_for_year, choices, help_text, db_column, db_tablespace, auto_created,
                                            validators, error_messages)
