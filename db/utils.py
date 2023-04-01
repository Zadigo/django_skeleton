# mimicks: django.db.utils

from functools import cached_property
from importlib import import_module

from asgiref.local import Local

DEFAULT_DB_ALIAS = 'default'


def load_backend(path):
    try:
        return import_module(path)
    except:
        raise ImportError('Backend does not exist')


class BaseConnectionHandler:
    thread_critical = False

    def __init__(self, settings=None):
        self._settings = settings
        self._connections = Local(self.thread_critical)

    def __getitem__(self, alias):
        try:
            connection = getattr(self._connections, alias)
        except AttributeError:
            pass
        connection = self.create_connection(alias)
        setattr(self._connections, alias, connection)
        return connection

    @cached_property
    def settings(self):
        self._settings = self.configure_settings(self._settings)
        return self._settings

    def configure_settings(self, settings):
        if settings is None:
            settings = {}
            settings['default'] = {}
        settings['default']['NAME'] = 'test.sqlite'
        settings['default']['ENGINE'] = 'django_skeleton.db.backends.sqlite'
        return settings

    def create_connection(self, alias):
        pass


class ConnectionHandler(BaseConnectionHandler):
    def configure_settings(self, settings):
        return super().configure_settings(settings)

    def create_connection(self, alias):
        db = self.settings[alias]
        backend = load_backend(db['ENGINE'])
        # from django.db import backends
        # FIXME: Cannot get .base from backend
        return backend.base.DatabaseWrapper(db, alias)
