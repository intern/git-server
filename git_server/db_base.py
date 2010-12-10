# -*- coding: utf-8 -*-
"""
API for Mysql database basic:

  db_affected_rows     Determine the number of rows changed by the preceding query.
  db_column_exists     Check if a column exists in the given table.
  db_connect           Initialise a database connection.
  db_decode_blob       Returns text from a Binary Large OBject value.
  db_distinct_field    Adds the DISTINCT flag to the supplied query and returns the altered query.
  db_encode_blob       Returns a properly formatted Binary Large Object value.
  db_error             Determine whether the previous query caused an error.
  db_escape_string     Prepare user input for use in a database query, preventing SQL injection attacks.
  db_escape_table      Restrict a dynamic table, column or constraint name to safe characters.
  db_fetch_hash        Fetch one result row from the previous query as an dict.
  db_is_active         Returns a boolean depending on the availability of the database.
  db_last_insert_id    Returns the last insert id. This function is thread safe.
  db_lock_table        Lock a table.
  db_placeholders      Generate placeholders for an array of query arguments of a single type.
  db_prefix_tables     Append a database prefix to all tables in a query.
  db_query             Runs a basic query in the active database.
  db_result            Return an individual result field from the previous query.
  db_set_active        Activate a database for future queries.
  db_status_report     Report database status.
  db_table_exists      Check if a table exists.
  db_unlock_tables     Unlock all locked tables.
  db_version           Returns the version of the database server currently in use.
"""

import ConfigParser

import MySQLdb

import re

# Globle the db link handle and table prefix
__DB = None

__DB_PREFIX = None

# Indicates the place holders that should be replaced in __db_query_callback()
DB_QUERY_REGEXP = '(%d|%s|%%|%f|%b|%n)'

# Safe characters for column, table or constraint name
DB_SAFE_CHARACTERS_REGEXP = '[^A-Za-z0-9_]+'

def get_db_config_file():
    config = ConfigParser.ConfigParser()
    # TODO fix the abs path
    config.read('/etc/git.conf')
    return config

def get_db_config():
    config = get_db_config_file()
    return __get_db_config(config)

def db_connect( ):
    __db_connect( **get_db_config() )

def db_query(query, *args):
    query = db_prefix(query)
    query = __db_query_callback(query, *args)
    return __db_query(query)

def db_affected_rows(cursor):
    return cursor.rowcount

def db_escape_string(string):
    return MySQLdb.escape_string(string)

def db_fetch_hash(cursor):
    record = cursor.fetchone()
    if record is None:
        cursor.close()
    return record

def db_prefix_tables():
    return __DB_PREFIX

#Lock the named table.
def db_lock_table(table):
    db_query('LOCK TABLES {' + db_escape_table(table) + '} WRITE')

# Unlock all locked tables.
def db_unlock_tables():
    db_query('UNLOCK TABLES')

def db_result(cursor):
    return __db_result(cursor)

def db_last_insert_id():
    return db_result(db_query('SELECT LAST_INSERT_ID()'))

def db_escape_table(name):
    pattern = re.compile(DB_SAFE_CHARACTERS_REGEXP)
    return re.sub(pattern, '', name)

def db_is_active():
    return bool(_DB.open)

# Returns the version of the database server currently in use.
#   @return Database server version
def db_version():
    return __db_version()

# Returns text from a Binary Large Object value.
#
#   @param $data
#     Data to decode.
#   @return
#     Decoded data.
def db_decode_blob(data):
    return data;

# Check if a table exists.
def db_table_exists(table):
    return db_fetch_hash(db_query("SHOW TABLES LIKE '{" + db_escape_table(table) + "}'"))

# tables implement prefix with config.ini
def db_prefix(query):
    return query.replace('{', db_prefix_tables()).replace('}', '')

def __db_connect( *args, **args_dict ):
    global __DB
    __DB = MySQLdb.connect( *args, **args_dict )
    if not args_dict.has_key('charset'):
        encoding = args_dict['charset']
    else:
        encoding = 'utf8'
    __DB.set_character_set( encoding )

def __db_query(query):
    print "LOG:: ", query
    cursor = __DB.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(query)
    return cursor

def __db_result(cursor):
    fetch = db_fetch_hash(cursor)
    if fetch and len(fetch):
        return fetch[fetch.keys()[0]]
    return None

# Helper function for db_query().
def __db_query_callback(query, *args):
    pattern = re.compile(DB_QUERY_REGEXP)
    # %s %d %% ... as list []
    holders = pattern.findall(query)
    if bool(holders):
        args = __db_query_args_to_tuple(*args)
        sql, i = list(), 0
        for holder in pattern.finditer(query):
            (a, b) = holder.span()
            sql.append(query[i:a])
            i = b
        sql.append(query[i:])
        return __db_query_sql_format(sql, holders, args)
    return query

def __db_query_args_to_tuple(*args):
    if len(args):
        if isinstance(args[0], tuple) or isinstance(args[0], list):
            args = tuple(args[0])
    return args

def __db_query_sql_format(slices, holders, args):
    for i, holder in enumerate(holders):
        slices[i] += __format(holder, args[i])
    return "".join(slices)

# TODO format the holder with arg
def __format(holder, arg):
    return db_escape_string(str(arg))

# Helper function for db_version
def __db_version():
    return __DB.get_server_info().split('-')[0]

def __get_db_config(config):
    global __DB_PREFIX
    db_conf = dict()
    db_conf['host']    = config.get('MYSQL', 'server'  )
    db_conf['user']    = config.get('MYSQL', 'username')
    db_conf['passwd']  = config.get('MYSQL', 'password')
    db_conf['port']    = config.getint('MYSQL', 'port' )
    db_conf['db']      = config.get('MYSQL', 'database')
    db_conf['charset'] = config.get('MYSQL', 'encoding')

    # Setting the table prefix
    __DB_PREFIX = config.get('MYSQL', 'prefix')
    return db_conf

if __name__ == '__main__':
   db_connect()
   db_query("insert into {role}(name) values('%s')",['alias heressss'])
   print db_last_insert_id()
   link = db_query("select * from {role} where rid > %d ", 10, 0, 'test key' )
   print 'db_result:', db_result(link)
   print "db_affected_rows:", db_affected_rows(link)
   while(True):
       r = db_fetch_hash(link)
       if r is None:
           break
       print r
   print 'db_version:', db_version()
   #get_db_config()
