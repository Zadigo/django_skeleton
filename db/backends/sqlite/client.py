from django_skeleton.db.backends.base.client import BaseDatabaseClient

class DatabaseClient(BaseDatabaseClient):
    @classmethod
    def settings_to_cmd_args_env(cls, settings_dict, parameters):
        # NOTE: In django, the settings dict is the settings dict
        # of the database {NAME: ..., ...} in settings.py
        args = [cls.executable_name, settings_dict['NAME'], *parameters]
        return args, None
