import os
import subprocess

class BaseDatabaseClient:
    executable_name = None
    
    def __init__(self, connection):
        # connection is an instance of BaseDatabaseWrapper.
        self.connection = connection

    @classmethod
    def settings_to_cmd_args_env(cls, settings_dict, parameters):
        pass
    
    def runshell(self, parameters):
        args, env = self.settings_to_cmd_args_env(self.connection.settings_dict, parameters)
        env = {**os.environ, **env} if env else None
        subprocess.run(args, env=env, check=True)
