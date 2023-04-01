# setup [entrypoint] -> apps [registry] <> settings
# model [structure] <-> manager [interface] <-> queryset [data] -> query [sql] <-> sqlcompiler -> connections -> databasewrapper -> database

# from django_structure.db.utils import connections
# from django_structure.db.backends.sqlite.base import DatabaseWrapper
# from django_structure.db.models.sql.query import Query
from django_skeleton.setup import setup

# w = DatabaseWrapper({'NAME': 'test.sqlite', 'ENGINE': None})
# w.connect()


# connections.create_connection('default')


# query = Query(type('Celebrity', (), {}))
# compiler = query.get_compiler(using='default')
# print(compiler)

setup()
from django_structure.db.models.models import Model
