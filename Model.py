import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

import QueryResult
from DataGenerator import DataGenerator
from static import DATABASE_NAME, DATABASE_LOGIN, DATABASE_PASSWORD, CREATE_TABLES


class SQL:
    def __init__(self):
        # connect to postgres
        self.conn = psycopg2.connect(
            user=DATABASE_LOGIN,
            password=DATABASE_PASSWORD
        )

        self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        if not self.db_exist():
            self.create_or_reset_db()
        else:
            self.reconnect_to_db()

        print('Connected successfully')

    def process_query(self, query):
        """Takes an SQL query and processes it"""
        cur = self.conn.cursor()
        result = QueryResult.QueryResult()
        try:
            cur.execute(query)
            result.column_names = [column.name for column in cur.description]
            result.values = cur.fetchall()
        except Exception as e:
            result.is_error = True
            result.exception = e
        return result

    def insert_random_data(self):
        cur = self.conn.cursor()
        queries = DataGenerator().generate()
        for query in queries:
            cur.execute(query)

    def generate_data(self):
        self.create_or_reset_db()
        cur = self.conn.cursor()
        queries = DataGenerator().generate()
        for x in queries:
            f = open('insertion.sql', 'w', encoding='utf-8')
            f.write(x)
            f.close()
            cur.execute(x)

        self.conn.commit()
        print("Committed successfully.")

        cur.close()

    def db_exist(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s;", [DATABASE_NAME])
        return cursor.fetchone()

    def reconnect_to_db(self):
        # reconnect to the database
        self.conn = psycopg2.connect(
            database=DATABASE_NAME,
            user=DATABASE_LOGIN,
            password=DATABASE_PASSWORD
        )
        self.conn.autocommit = True

    def reconnect_to_server(self):
        self.conn.commit()
        self.conn = psycopg2.connect(
            user=DATABASE_LOGIN,
            password=DATABASE_PASSWORD
        )
        self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    def create_or_reset_db(self):
        self.reconnect_to_server()
        cursor = self.conn.cursor()
        cursor.execute(sql.SQL("DROP DATABASE IF EXISTS {};").format(sql.Identifier(DATABASE_NAME)))
        cursor.execute(sql.SQL("CREATE DATABASE {};").format(sql.Identifier(DATABASE_NAME)))

        self.reconnect_to_db()
        cursor = self.conn.cursor()
        cursor.execute(CREATE_TABLES)
