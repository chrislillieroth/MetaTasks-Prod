#!/usr/bin/env python
import os, time, sys
import psycopg

def main():
    host = os.getenv('DB_HOST','db')
    port = int(os.getenv('DB_PORT','5432'))
    user = os.getenv('DB_USER','metatasks')
    password = os.getenv('DB_PASSWORD','metatasks')
    dbname = os.getenv('DB_NAME','metatasks')
    dsn = f'dbname={dbname} user={user} password={password} host={host} port={port}'
    max_attempts = 60
    for attempt in range(1, max_attempts+1):
        try:
            with psycopg.connect(dsn, connect_timeout=2) as conn:
                with conn.cursor() as cur:
                    cur.execute('SELECT 1')
                    print('Database is ready')
                    return 0
        except Exception as e:
            print(f'[{attempt}/{max_attempts}] Database not ready: {e.__class__.__name__}: {e}')
            time.sleep(1)
    print('Database not ready after waiting, exiting.', file=sys.stderr)
    return 1

if __name__ == '__main__':
    raise SystemExit(main())
