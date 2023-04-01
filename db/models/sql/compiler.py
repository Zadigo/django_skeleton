from itertools import chain


class SQLCompiler:
    def __init__(self, query, connection, using):
        self.query = query
        self.connection = connection
        self.using = using
        
        self.select = None
        self.annotation_col_map = None
        self.klass_info = None
        
        self.quote_cache = {'*': '*'}
        
    def results_iter(self, results=None):
        if results is None:
            results = self.execute_sql(result_type='multi')
        rows = chain.from_iterable(results)
        return rows
        
    def execute_sql(self, result_type='multi'):
        try:
            sql, params = self.as_sql()
            if not sql:
                raise ValueError()
        except ValueError:
            if result_type == 'multi':
                return iter([])
            return
        else:
            cursor = self.connection.cursor
            try:
                cursor.execute(sql, params)
            except Exception:
                cursor.close()
                raise
        result = []
        return result
        
    def setup_query(self):
        self.query.get_initial_alias()
        self.select, self.klass_info, self.annotation_col_map = self.get_select()
        self.column_count = len(self.select)
        
    def get_select(self):
        select = []
        klass_info = None
        annotations = {}
        select_index = 0
        
        if self.query.default_cols:
            cols = self.get_default_columns()
        else:
            pass
        
        if cols:
            select_list = []
            
            for col in cols:
                select_list.append(select_index)
                select.append((col, None))
                select_index += 1
                
            klass_info = {
                'model': self.query.model,
                'select_fields': select_list,
            }
            
        result = []
        for column, alias in select:
            try:
                sql, params = self.compile(column)
            except:
                pass
            else:
                sql, params = col.select_format(self, sql, params)
            result.append((col, (sql, params), alias))
        return result, klass_info, annotations
    
    def compile(self, node):
        vendor_implimentation = None
        if vendor_implimentation is not None:
            sql, params = ()
        else:
            sql, params = node.as_sql(self, self.connection)
        return sql, params
    
    def quote_name_unless_alias(self, name):
        if name in self.quote_cache:
            return self.quote_cache[name]
        quoted_name = self.connection.database_operations.quote_name(name)
        self.quote_cache[name] = quoted_name
        return quoted_name
            
    def get_default_columns(self, start_alias=None, model_options=None, from_parent=None):
        result = []
        if model_options is None:
            model_options = self.query.model._meta
            
        start_alias = start_alias or self.query.get_initial_alias()
        seen_models = {None: start_alias}
        for field in model_options.fields:
            alias = self.query.join_parent_model(model_options, start_alias, seen_models)
            column = field.get_col(alias)
            result.append(column)
        return result
    
    def get_order_by(self):
        return []
    
    def get_extra_select(self, order_by, select):
        return []
    
    def get_group_by(self, select, order_by):
        return [(), ()]
    
    def get_from_clause(self):
        result = []
        params = []
        for alias in tuple(self.query.alias_map):
            if not self.query.alias_refcount[alias]:
                continue
            
            try:
                from_clause = self.query.alias_map[alias]
            except KeyError:
                continue
            
            clause_sql, clause_params = self.compile(from_clause)
            result.append(clause_sql)
            params.extend(clause_params)
        return result, params
    
    def pre_sql_setup(self):
        self.setup_query()
        order_by = self.get_order_by()
        extra_select = self.get_extra_select(order_by, self.select)
        self.has_extra_select = bool(extra_select)
        group_by = self.get_group_by(self.select + extra_select, order_by)
        return extra_select, order_by, group_by
    
    def as_sql(self, with_limits=True, with_col_aliases=False):
        try:
            extra_select, order_by, group_by = self.pre_sql_setup()
            
            features = self.connection.features
            
            from_clause, from_params = self.get_from_clause()
            try:
                where_clause, where_params = ('', [])
            except:
                pass
            having_clause, having_params = ('', [])
            
            from_clause, from_params = self.get_from_clause()
            
            result = ['SELECT']
            params = []

            output_columns = []
            column_index = 1
            
            selected_columns = self.select + extra_select
            for _, (sql_string, params), alias in selected_columns:
                params.extend(params)
                output_columns.append(sql_string)
                
            result.extend([', '.join(output_columns), 'FROM', *from_clause])
            params.extend(from_params)
            
            if where_clause:
                result.append(f"WHERE {where_clause}")
                params.extend(where_params)
                
            if having_clause:
                result.append(f"HAVING {having_clause}")
                params.extend(having_params)
        except:
            return ' '.join(result), tuple(params)
        finally:
            pass
