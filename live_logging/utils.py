# -*- coding: utf-8 -*-
import logging
from django.conf import settings


def tree():
    """Return a tree of tuples representing the logger layout.
    Each tuple looks like ``('logger-name', <Logger>, [...])`` where the
    third element is a list of zero or more child tuples that share the
    same layout.
    """
    root = ('', logging.root, [])
    nodes = {}
    items = list(logging.root.manager.loggerDict.items())  # for Python 2 and 3
    items.sort()
    for name, logger in items:
        nodes[name] = node = (name, logger, [])
        i = name.rfind('.', 0, len(name) - 1)  # same formula used in `logging`
        if i == -1:
            parent = root
        else:
            parent = nodes[name[:i]]
        parent[2].append(node)
    return root


def read_config():
    from .models import Handler, Formatter, Logger

    for k, v in settings.LOGGING.get('formatters', {}).items():
        __, new = Formatter.objects.get_or_create(name=k, defaults=v)

    for k, v in settings.LOGGING.get('handlers', {}).items():
        __, new = Handler.objects.get_or_create(name=k, defaults={
            'level': logging._levelNames.get(v['level'], 'NOTSET'),
            'handler': v.get('class', ''),
            'formatter': Formatter.objects.get_or_create(name=v.get('formatter', 'simple'), defaults={'format': ''})[0]
        })

    for k, v in settings.LOGGING.get('loggers', {}).items():
        lg, new = Logger.objects.get_or_create(name=k, defaults={
            'level': logging._levelNames.get(v['level'], logging.NOTSET),
            'propagate': v.get('propagate', False),
        })
        if v['handlers']:
            for h in v['handlers']:
                lg.handlers.add(Handler.objects.get(name=h))
            lg.save()



def get_test_logger(level):
    from handlers import DjangoDatabaseHandler

    formatter = logging.Formatter('%(asctime)-6s: %(name)s - %(levelname)s - %(message)s')
    handler = DjangoDatabaseHandler(level)
    handler.setFormatter(formatter)

    logger = logging.getLogger("test-logging")
    logger.propagate = False

    logger.addHandler(handler)
    logger.setLevel(level)
    return logger


def logdb(msg, level=logging.DEBUG):
    logger = get_test_logger(level)
    logger.log(level, msg)

