# -*- coding: utf-8 -*-
from django.apps import AppConfig as AC
from django.db.utils import ProgrammingError, OperationalError



class AppConfig(AC):
    name = 'live_logging'
    label = 'live_logging'
    verbose_name = 'Logging'

    def ready(self):
        from live_logging.models import apply_config
        from live_logging.utils import logdb
        try:
            apply_config()
            logdb('Database logging configuration applied')
        except (ProgrammingError, OperationalError):
            pass
