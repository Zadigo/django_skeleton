from sqlite3 import dbapi2 as Database

from django_skeleton.db.backends.base.base import BaseDatabaseWrapper
from django_skeleton.db.backends.sqlite.client import DatabaseClient
from django_skeleton.db.backends.sqlite.operations import DatabaseOperations
from django_skeleton.db.backends.sqlite.schema import DatabaseSchemaEditor


class DatabaseWrapper(BaseDatabaseWrapper):
    vendor = 'sqlite'
    display_name = 'SQLite'
    data_types = {
        'AutoField': 'integer',
        'CharField': 'varchar({max_length})'
    }
    operators = {
        'exact': '= {value}'
    }
    Database = Database
    SchemaEditor = DatabaseSchemaEditor
    database_operations_class = DatabaseOperations
    # NOTE: Database operations in CMD ?
    client_class = DatabaseClient

    def connection_parameters(self):
        return {
            'database': self.settings_dict['NAME']
        }

    def get_new_connection(self, connection_params):
        connection = Database.connect(**connection_params)
        return connection
