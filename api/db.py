import time

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

class Connection(object):
  def __init__(self, host, user, password):
    self.db = None
    dbname = "rxdb" # TODO: Make this configurable
    params = 'host={} dbname={} user={} password={} connect_timeout=3'.format(host, dbname, user, password)
    connect = self._attempt_connect(params, 3, 10)
    print("Connected!")
    self.cursor = self.db.cursor()
  
  # TODO: This thing is just for demo purposes. If the API starts
  # but there's no DB, it dies and won't restart. This is probably
  # not good.
  def _attempt_connect(self, params, pause, max_tries, attempts=0):
    attempts += 1
    print("Connecting. Attempt {} of {}.".format(attempts, max_tries))
    try:
      self.db = psycopg2.connect(params)
    except:
      if attempts >= max_tries:
        print("Giving up.")
        exit(1)
      print("Connection to DB failed. Retrying in {} seconds.".format(pause))
      time.sleep(pause)
      self._attempt_connect(params, pause, max_tries, attempts)

  def fetch_db_tables(self):
    tables = []
    with self.db.cursor() as cursor:
      try:
        cursor.execute("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public';")
        for result in cursor:
          tables.append(result[0])
      finally:
        self.db.commit()
    return tables

  def fetch_table_data(self, table):
    headers = []
    data = []
    with self.db.cursor() as cursor:
      try:
        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name='{}';".format(table))
        for result in cursor:
          headers.append(result[0])
        cursor.execute("SELECT * FROM {};".format(table))
        for result in cursor: # can't just return the cursor; it's closed when this function returns
          data.append(result)
      finally:
        self.db.commit()
      return headers, data
  
  def read(self, query):
    results = []
    with self.db.cursor() as cursor:
      cursor.execute(query)
      for result in cursor:
        results.append(result)
    return results

  def __del__(self):
    if self.db is not None:
      self.db.close()