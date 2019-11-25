from os.path import dirname
from pathlib import Path

# WARNING! AUTO-GENERATED CONSTANTS! DO NOT CHANGE THEM!
PATH = Path(dirname(__file__))

DATABASE_SCHEMA_FILE = PATH / "SQL" / "init.sql"
QUERY1_FILE = PATH / "SQL" / "query1.sql"
QUERY2_FILE = PATH / "SQL" / "query2.sql"
QUERY3_FILE = PATH / "SQL" / "query3.sql"
QUERY4_FILE = PATH / "SQL" / "query4.sql"
QUERY5_FILE = PATH / "SQL" / "query5.sql"

with open(DATABASE_SCHEMA_FILE, encoding="utf-8") as f:
    CREATE_TABLES = f.read()

with open(QUERY1_FILE, encoding="utf-8") as f:
    QUERY1 = f.read()

with open(QUERY2_FILE, encoding="utf-8") as f:
    QUERY2 = f.read()

with open(QUERY3_FILE, encoding="utf-8") as f:
    QUERY3 = f.read()

with open(QUERY4_FILE, encoding="utf-8") as f:
    QUERY4 = f.read()

with open(QUERY5_FILE, encoding="utf-8") as f:
    QUERY5 = f.read()
