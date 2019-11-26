import inspect
import os
import sqlite3
import sys

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from DataGenerator import DataGenerator
from DataGenerator.static import PATH

# create data
dg = DataGenerator()
sql = "".join(dg.generate())

for df in [(PATH.parent / "SQL" / "pg_dump.sql", PATH.parent / "SQL" / "init.sql"),
           (PATH.parent / "SQL" / "ms_dump.sql", PATH.parent / "SQL" / "init_mysql.sql")]:
    with open(df[0], "w", encoding='utf-8') as dump:
        dump.write("--Creating tables\n")
        with open(df[1], "r", encoding='utf-8') as init:
            dump.write(init.read())
        dump.write("--Insertions\n")
        dump.write(sql)

# testing
print("Starting posrgres dump file testing...")
conn = psycopg2.connect(
    user="postgres",
    password="root1234"
)
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
conn.autocommit = True
cur = conn.cursor()
cur.execute("DROP DATABASE IF EXISTS test213213;")
cur.execute("CREATE DATABASE test213213;")
conn.close()

conn = psycopg2.connect(
    database="test213213",
    user="postgres",
    password="root1234"
)
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
conn.autocommit = True
with open(PATH.parent / "SQL" / "pg_dump.sql", encoding='utf-8') as f:
    conn.cursor().execute(f.read())
print("postgres works!")
conn.close()

print("starting testing sqlite")
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()
with open(PATH.parent / "SQL" / "ms_dump.sql", encoding='utf-8') as f:
    # a = f.read().split(";")
    # for aa in a:
    #     cursor.execute(aa)
    cursor.executescript(f.read())
conn.commit()
cursor.execute("SELECT * FROM general_user;")
print(cursor.fetchall())
print("sqlite works!")
