import sqlite3
import os

DB_PATH = os.getenv('DATABASE_PATH', 'recipes.db')
SCHEMA_FILE = 'schema.sql'

if not os.path.exists(SCHEMA_FILE):
    print('schema.sql not found in current directory')
    raise SystemExit(1)

conn = sqlite3.connect(DB_PATH)
with open(SCHEMA_FILE, 'r', encoding='utf-8') as f:
    sql = f.read()
conn.executescript(sql)
conn.commit()
conn.close()
print(f'Created {DB_PATH} using {SCHEMA_FILE}')
