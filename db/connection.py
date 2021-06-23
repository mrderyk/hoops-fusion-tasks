import os, urllib.parse
from playhouse.postgres_ext import PostgresqlExtDatabase

DATABASE_URL = os.environ['DATABASE_URL']
url = urllib.parse.urlparse(DATABASE_URL)

db = PostgresqlExtDatabase(
  url.path[1:],
  user=url.username,
  host=url.hostname,
  port=url.port,
  password=url.password,
  register_hstore=False
)