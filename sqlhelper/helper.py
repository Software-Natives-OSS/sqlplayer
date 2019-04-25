#
# Copyright zulli73@gmail.com. All Rights Reserved.
#
# Use of this source code is governed by the MIT license
#
import os
import re
import json
# Download it at http://sourceforge.net/projects/mysql-python/?source=dlp
# Tutorials: http://mysql-python.sourceforge.net/MySQLdb.html
#            http://zetcode.com/db/mysqlpython/
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
import datetime, time

VERBOSE = False
# globally remember the currently active delimiter
current_delimiter = ';'
re_delimiter = re.compile(r'^[\s]*delimiter[\s]*(.*)$')

def read_opts(location):
    '''
    Searches for a 'mysql.json' file at the current location and all it's parents.
    Stops as soon as the first such file was found. As the file name suggests, the
    content of that file must be valid JSON. Otherwise, this function will fail
    with an exception.
    '''
    cur_dir = os.path.abspath(location)
    while True:
        file_list = os.listdir(cur_dir)
        parent_dir = os.path.dirname(cur_dir)
        if 'mysql.json' in file_list:
            full_location = os.path.join(cur_dir, 'mysql.json')
            print("Loading MySQL options file from '{}'".format(full_location))
            return json.load(open(full_location, 'r'))
        else:
            if cur_dir == parent_dir:
                raise Exception("no mysql.json found")
            else:
                cur_dir = parent_dir


def create_connection(opts):
    try:
        return mysql.connector.MySQLConnection(**opts)
    except Error as e:
        raise Exception(str(e))

def close_connection(connection):
    connection.close()


def handle_delimiter(line):
    ''' Handle some uglyness: We need to filter 'delimiter XYZ' statements, as
    this mysql client can't deal with it.

    Moreover, when this newly defined 'delimiter pattern' (the XYZ) is actually
    used, we need to replace it by the normal ';'. This handling is most probably
    not fully perfect, but works for the so far tested use cases.
    '''
    global current_delimiter
    m = re_delimiter.match(line.lower())
    if m:
        current_delimiter = m.group(1)
        return ''
    elif line.strip().endswith(current_delimiter):
        return line.replace(current_delimiter, ';')
    else:
        return line


def run_sql_file(filename, connection, sql_statements_log):
    '''
    The function takes a filename and a connection as input
    and will run the SQL query on the given connection  
    '''

    start = time.time()
    sql_statements_log.write('\n\n-- Executing {}\n\n'.format(os.path.basename(filename)))
    
    file = open(filename, 'r')
    # Note: some file may contain 'delimiter' statements. While these are 
    # crucial for e.g. MySQL workbench, they are not supported by this "Python
    # MySQL client". Therefore, we have to ensure to not execute them in this
    # context, but leave them in the 'Overall log file', which may later be
    # used by the Workbench
    original_sql = sql =''
    for line in file.readlines():
        original_sql += line
        sql += handle_delimiter(line)
    print("\tStart executing: '{}'".format(filename))
    if VERBOSE:
        print(sql)
    cursor = connection.cursor()
    for _ in cursor.execute(sql, multi=True):
        pass
    connection.commit()
    
    end = time.time()
    print("\tTime elapsed to run the query: {} ms".format(str((end - start)*1000)))

    sql_statements_log.write(original_sql)
