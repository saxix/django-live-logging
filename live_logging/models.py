import logging
import django
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .fields import JSONField, TupleField
from live_logging import fields

LOG_LEVELS = (
    (logging.INFO, 'Info'),
    (logging.WARNING, 'Warning'),
    (logging.DEBUG, 'Debug',),
    (logging.ERROR, 'Error'),
    (logging.CRITICAL, 'Critical'),
)

LOG_RECORD_RESERVED_ATTRS = (
    'args',  # Always a tuple.
    'created',
    'exc_info',  # "Something" that evaluates to True or False.
    'exc_text',
    'filename',
    'funcName',
    'levelname',
    'levelno',
    'lineno',
    'module',
    'msecs',
    'msg',
    'name',
    'pathname',
    'process',
    'processName',
    'relativeCreated',
    'thread',
    'threadName',
    # Additional:
    'message',
    'asctime',
)


class LogManager(models.Manager):
    def _get_extra(self, record):
        """
        Get the extra fields by filtering out the known reserved fields.

        Note: Values are stringified to prevent deep pickling.
        """
        extra = {}
        for k, v in record.__dict__.items():
            if k not in LOG_RECORD_RESERVED_ATTRS:
                extra[k] = unicode(v)  # Stringify
        return extra

    def create_from_record(self, record):
        """
        Creates an error log for a `logging` module `record` instance. This is
        done with as little overhead as possible.

        NOTE: The message and message arguments are stringified in case odd
        objects are passed, even though this should be up to the user.
        """
        # Try to convert all arguments to unicode.
        try:
            args = map(unicode, record.args)
        except UnicodeDecodeError:
            args = []
            for arg in record.args:
                try:
                    args.append(unicode(arg))
                except UnicodeDecodeError:
                    # If a specific argument goes wrong, try to replace the
                    # invalid characters.
                    try:
                        args.append(unicode(arg, errors='replace'))
                    except:
                        args.append(u'(django-live-logging: Argument encoding error)')
                except:
                    args.append(u'(django-live-logging: Incorrect argument)')

        # Try to convert the message to unicode.
        try:
            msg = unicode(record.msg)
        except UnicodeDecodeError:
            try:
                msg = unicode(record.msg, errors='replace')
            except:
                msg = u'(django-live-logging: Message encoding error)'

        log_entry = LogEntry.objects.create(
            args=tuple(args),
            exc_text=record.exc_text,
            filename=record.filename,
            function_name=record.funcName,
            level=record.levelno,
            line_number=record.lineno,
            module=record.module,
            msg=msg,
            name=record.name,
            path=record.pathname,
            process=record.process,
            process_name=record.processName if hasattr(record, 'processName') else None,
            thread=record.thread,
            thread_name=record.threadName,
            extra=self._get_extra(record),
        )
        return log_entry


class BaseLogEntry(models.Model):
    """
    Basic log entry fields.
    """
    filename = models.CharField(max_length=50, blank=True, null=True)
    function_name = models.CharField(max_length=50, blank=True, null=True)
    level = models.PositiveIntegerField(choices=LOG_LEVELS, default=logging.CRITICAL, db_index=True)
    line_number = models.PositiveIntegerField(default=0)
    module = models.CharField(max_length=50, blank=True, null=True)
    msg = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=200, default='root', db_index=True)
    path = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        abstract = True


class LogEntry(BaseLogEntry):
    """
    Represents a single log entry from the `logger` module. Most of the `logger`
    fields are represented in this model, except for some time related fields.
    """
    args = TupleField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    exc_text = models.TextField(blank=True, null=True)
    process = models.PositiveIntegerField(default=0)
    process_name = models.CharField(max_length=200, blank=True, null=True)
    thread = models.DecimalField(max_digits=21, decimal_places=0)
    thread_name = models.CharField(max_length=200, blank=True, null=True)
    extra = JSONField(blank=True)

    objects = LogManager()

    class Meta:
        verbose_name_plural = _('Log entries')
        if django.VERSION >= (1, 7):
            default_permissions = ('delete', )

    def get_message(self):
        if not self.args:
            return self.msg

        try:
            return self.msg % self.args
        except TypeError, e:
            return u'Failed to render message: %s' % e

    def get_message_display(self):
        msg = self.get_message()
        if len(msg) > 40:
            return u'%s [...]' % msg[:35]
        else:
            return u'%s' % msg

    get_message_display.short_description = _('message')

    def __unicode__(self):
        return self.get_message_display()


class Formatter(models.Model):
    name = models.CharField(max_length=100, unique=True)
    format = models.CharField(max_length=200)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name


class Handler(models.Model):
    name = models.CharField(max_length=100, unique=True)
    level = fields.LogLevelField()
    handler = models.CharField(max_length=255)
    formatter = models.ForeignKey(Formatter)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name


class Logger(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=True)
    handlers = models.ManyToManyField(Handler, related_name='handlers')
    propagate = models.BooleanField(default=False)
    level = fields.LogLevelField()

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name


def apply_config(limit_to=None):
    from django.conf import settings

    limit_to = limit_to or [Formatter, Handler, Logger]
    if Formatter in limit_to:
        formatters = settings.LOGGING.get('formatters', [])
        for formatter in Formatter.objects.all():
            formatters[formatter.name]['format'] = formatter.format

    if Handler in limit_to:
        handlers = settings.LOGGING.get('handlers', [])
        for handler in Handler.objects.all():
            handlers[handler.name]['level'] = handler.level
            # handlers[handler.name]['class'] = handler.handler
            handlers[handler.name]['formatter'] = handler.formatter.name

    if Logger in limit_to:
        loggers = settings.LOGGING.get('loggers', [])
        for logger in Logger.objects.all():
            if logger.name not in loggers:
                loggers[logger.name] = {}
            loggers[logger.name]['propagate'] = logger.propagate
            loggers[logger.name]['handlers'] = logger.handlers.values_list('name', flat=True)
            loggers[logger.name]['level'] = logger.level

    logging.config.dictConfig(settings.LOGGING)
