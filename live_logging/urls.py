# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from live_logging.views import LoggingConfigView

urlpatterns = patterns('',
                       url(r'^$', LoggingConfigView.as_view(), name='logging-conf'),
                       )
