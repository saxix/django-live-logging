from __future__ import unicode_literals
import logging
from django.conf.urls import url
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from functools import update_wrapper
from django.conf.urls import patterns
from django.contrib.admin import site
from live_logging.handlers import DjangoDatabaseHandler
from live_logging.utils import read_config, get_test_logger
from .models import LogEntry, Formatter, Handler, Logger, apply_config
from django.contrib import admin




class LogEntryAdmin(admin.ModelAdmin):
    # change_form_template = 'admin/logging/error_form.html'
    list_display = (
        'created', 'level', 'name', 'module', 'function_name', 'line_number', 'process', 'thread',
        'get_message_display')
    # readonly_fields = (name for name in LogEntry._meta.fields)
    list_filter = ('name', 'level', 'created')
    date_hierarchy = 'created'
    ordering = ('-created',)
    actions_on_top = True

    def has_add_permission(self, request):
        return False

    def suit_row_attributes(self, obj, request):
        css_class = {
            logging.INFO: 'info',
            logging.WARN: 'warning',
            logging.CRITICAL: 'error',
            logging.ERROR: 'error',
        }.get(obj.level, None)
        if css_class:
            return {'class': css_class, 'data': obj.name}

    def get_urls(self):
        original = super(LogEntryAdmin, self).get_urls()

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)

            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.model_name

        return patterns('',
                        url(r'^log-test/$',
                            wrap(self.log_test),
                            name='%s_%s_test' % info), ) + original

    def _get_test_logger(self):
        return get_test_logger(logging.DEBUG)

    def log_test(self, request):
        test_logger = self._get_test_logger()
        test_logger.info('test INFO')
        test_logger.error('test ERROR')
        test_logger.warn('test WARN')
        test_logger.critical('test CRITICAL')
        test_logger.debug('test DEBUG')
        try:
            raise Exception('test EXCEPTION')
        except Exception as e:
            test_logger.exception(e)
        self.message_user(request, 'Emitted 6 log')
        info = self.model._meta.app_label, self.model._meta.model_name
        return HttpResponseRedirect(reverse('admin:%s_%s_changelist' % info))

    def get_changelist(self, request, **kwargs):
        return super(LogEntryAdmin, self).get_changelist(request, **kwargs)


class RefreshAdmin(admin.ModelAdmin):
    # change_list_template = 'admin/logging/change_list.html'

    def get_urls(self):
        original = super(RefreshAdmin, self).get_urls()

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)

            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.model_name

        return patterns('',
                        url(r'^refresh/$',
                            wrap(self.refresh),
                            name='%s_%s_refresh' % info), ) + original

    def refresh(self, request):
        try:
            read_config()
        except Exception as e:
            self.message_user(request, str(e)[:100], level=messages.ERROR)

        info = self.model._meta.app_label, self.model._meta.model_name
        return HttpResponseRedirect(reverse('admin:%s_%s_changelist' % info))

    def response_change(self, request, obj):
        apply_config()
        return super(RefreshAdmin, self).response_change(request, obj)


class FormatterAdmin(RefreshAdmin):
    list_display = ('name', 'format')


class HandlerAdmin(RefreshAdmin):
    list_display = ('name', 'level', 'handler', 'formatter')
    list_editable = ('level',)
    list_filter = ('level',)
    readonly_fields = ('handler',)
    search_fields = ('name',)


class LoggerAdmin(RefreshAdmin):
    list_display = ('name', 'level', 'propagate', 'handlers_list')
    list_editable = ('level',)
    list_filter = ('level',)
    search_fields = ('name',)

    def handlers_list(self, obj):
        return ','.join(obj.handlers.values_list('name', flat=True))

    handlers_list.verbose_name = 'Handlers'


admin.site.register(LogEntry, LogEntryAdmin)
site.register(Formatter, FormatterAdmin)
site.register(Handler, HandlerAdmin)
site.register(Logger, LoggerAdmin)

