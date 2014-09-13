# -*- coding: utf-8 -*-
from django.views.generic.base import TemplateView


class LoggingConfigView(TemplateView):
    template_name = 'admin/live_logging/config.html'
