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
  db_fetch_array       Fetch one result row from the previous query as an array.
  db_fetch_object      Fetch one result row from the previous query as an object.
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
#
#import ConfigParser

import MySQLdb

# Globle the db link handle and init
__DB = None


def db_connect( *args, **args_dict ):
    __db_connect( *args, **args_dict )


def __db_connect( *args, **args_dict ):
    global __DB
    __DB = MySQLdb.connect( *args, **args_dict )

def __db_version():
    pass




