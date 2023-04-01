from db.utils import DEFAULT_DB_ALIAS

class BaseDatabaseWrapper:
    vendor = None
    data_types = {}
    operators = {}
    display_name = None
    client_class = None
    database_operations_class = None
    
    def __init__(self, settings_dict, alias=DEFAULT_DB_ALIAS):
        self.connection = None
        self.settings_dict = settings_dict
        self.alias = alias
        self.close_at = None
        self.client = self.client_class(self)
        self.database_operations = self.database_operations_class(self)
        
    def connection_parameters(self):
        pass
    
    def get_new_connection(self, connection_params):
        pass
    
    def init_connection_state(self):
        pass

    def connect(self):
        max_age = None
        self.close_at = None if max_age is None else 4000
        connection_params = self.connection_parameters()
        self.connection = self.get_new_connection(connection_params)
