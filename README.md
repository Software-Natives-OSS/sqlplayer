# SQL Player

SQL Player is a small Python application that runs `.sql` files against a SQL database. Right now, only MySQL is supported.

It depends on Python 3.x and `mysql-connector-python` and is licensed under MIT.

## Quick Start

Install the required dependencies and run the script against a folder that contains files named like `01_firstfile.sql`, `34_AnotherFile.sql`, etc. (i.e. `*_*.sql`)

``` (shell)
# Create the configuration file to connect to the SQL database !!! ADJUST THE VALUES TO YOUR NEEDS !!!
{ echo '{ "host": "localhost", "port": 3306, "user": "root", "password": "rootroot"}'; } > mysql.json

# Create a small SQL file
{ echo 'CREATE DATABASE MyQLPlayer_test'; } > 01_test.sql
```

``` (shell)
pip install mysql-connector-python
python sqlplay.py ./sql-folder
```

## Introduction

The purpose of the player is to automatically execute an arbitrary count of SQL statements. Each `.sql` file can contain as many SQL statements as desired. This allows to put related SQL statements into one file. Because the player supports multiple files to be executed in-order, unrelated SQL statements can be put into other files.

This allows to properly organize a large project into several files which increases readability. Beside readability, the player supports the user in a  fast dev-rountrip as all these files can easily be executed by a simple command. Finally, it guarantees consistency among various runs, as everything happens automated as oposed to run `.sql` files in graphical tools "manually".

There are two modes of operation:

1. Execute single `.sql` files
2. Execute multiple `.sql` files, a so called "play book"

Each `.sql` file is called a "task". A play book is a file system folder, which contains `.sql` files that follow a certain naming convention. Therefore, a play book consist of multiple tasks.

If run against a play book, it searches for files starting with an "order prefix" and a "descripitive name" which are separated by an underscore: `*_*.sql`, e.g. `01_File1.sql` or `67_File67.sql`, as well as `00A_FileA.sql` and `ABC_AnotherFile.sql`. Searching for such files happens non-recursively! The found files are sorted alphanumerically and are then executed 'in order'.

## Logging

Whenever one or multiple `.sql` files are exeucted, the content of all of them are put into the file `Overall.sql` either next to the single `.sql` file or inside the play book folder, depending how you execute SQL Player.

This file serves two purposes:

- It can be used as a log file, e.g. for documentation purposes
- If the same SQL statements need to be executed on another system, where the player may not be available, that file may become handy

## Database connection

The database connection details, such as 'host', 'username' and 'password' are configured in a file named `mysql.json`, which must be a valid `.json` file. The properties of that json object will be passed to `mysql.connector.MySQLConnection` as is and therefore should contain the properties accepted by that function. Here's a valid example of such a file:

``` (json)
{
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "rootroot"
}
```

The SQL player starts searches for the `mysql.json` file at the location of the `.sql` file or at the location of the "play book" and continues to search for such a file going up the filesystem hierarchy unless one is found. This is similar as `Git` does it when looking for a `.gitignore` file.
