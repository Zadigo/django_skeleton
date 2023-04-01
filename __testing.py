# setup [entrypoint] -> apps [registry] <> settings
# model [structure] <-> manager [interface] <-> queryset [data] -> query [sql] <-> sqlcompiler -> connections -> databasewrapper -> database

# from django_skeleton.db.utils import connections
# from django_skeleton.db.backends.sqlite.base import DatabaseWrapper
from django_skeleton.db.models.sql.query import Query
from django_skeleton.db.models.models import Model
from django_skeleton.setup import setup

# w = DatabaseWrapper({'NAME': 'test.sqlite', 'ENGINE': None})
# w.connect()


# connections.create_connection('default')

fake_model = type('Celebrity', (), {})
query = Query(fake_model)
compiler = query.get_compiler(using='default')
print(compiler)

setup()
