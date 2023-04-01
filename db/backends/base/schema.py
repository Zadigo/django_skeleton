class BaseDatabaseSchemaEditor:
    sql_create_table = "CREATE TABLE %(table)s (%(definition)s)"

    def __init__(self, connection, collect_sql=False, atomic=True):
        self.connection = connection
        
    def table_sql(self, model):
        """Take a model and return its table definition."""
        sql = ''
        params = ()
        return sql, params
    
    def create_model(self, model):
        """
        Create a table and any accompanying 
        indexes or unique constraints for 
        the given `model`.
        """
        sql, params = self.table_sql(model)
        self.execute(sql, params or None)

    def execute(self, sql, params=()):
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
