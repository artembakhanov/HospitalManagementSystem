import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

import QueryResult
from DataGenerator import DataGenerator
from config import DATABASE_NAME, DATABASE_LOGIN, DATABASE_PASSWORD
from static import CREATE_TABLES


class SQL:
    """
    This class represents an interface for communicating between user and the database.
    """
    conn = None

    def __init__(self):
        # connect to postgres
        self.connect_to_server()
        self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        # create database if it does not exist
        if not self.db_exist():
            self.create_or_reset_db()
        else:

            self.connect_to_db()

        print('Connected successfully')

    def process_query(self, query):
        """
        Takes a query (string) and returns the result from the database.
        :param query: string query
        :return: result of the query
        """
        # getting cursor
        cur = self.conn.cursor()
        # initialize a QueryResult instance
        result = QueryResult.QueryResult()
        # try to execute the query and fetch the result
        try:
            cur.execute(query)
            result.column_names = [column.name for column in cur.description]
            result.values = cur.fetchall()
        except Exception as e:
            result.is_error = True
            result.exception = e
        return result

    def populate_database(self):
        """
        Populate database with random data.
        """
        self.create_or_reset_db()
        cur = self.conn.cursor()
        # generate queries
        queries = DataGenerator().generate()
        for query in queries:
            # insert each query
            cur.execute(query)
        cur.close()
        print("Populated successfully.")

    def generate_data(self):
        """
        WARNING! DEPRECATED METHOD!
        Use populate_database instead.

        Populate database with random data.
        """
        self.create_or_reset_db()
        cur = self.conn.cursor()
        queries = DataGenerator().generate()
        for x in queries:
            # f = open('insertion.sql', 'w', encoding='utf-8')
            # f.write(x)
            # f.close()
            cur.execute(x)

        print("Committed successfully.")

        cur.close()

    def db_exist(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s;", [DATABASE_NAME])
        return cursor.fetchone()

    def connect_to_db(self):
        """
        Connect to the database.
        :return:
        """
        self.conn = psycopg2.connect(
            database=DATABASE_NAME,
            user=DATABASE_LOGIN,
            password=DATABASE_PASSWORD
        )
        self.conn.autocommit = True

    def connect_to_server(self):
        """
        Connect to postgres.
        """
        self.conn = psycopg2.connect(
            user=DATABASE_LOGIN,
            password=DATABASE_PASSWORD
        )
        self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self.conn.autocommit = True

    def create_or_reset_db(self):
        """
        Creates or resets the database.
        """
        self.connect_to_server()
        cursor = self.conn.cursor()

        # recreate the database
        cursor.execute(sql.SQL("DROP DATABASE IF EXISTS {};").format(sql.Identifier(DATABASE_NAME)))
        cursor.execute(sql.SQL("CREATE DATABASE {};").format(sql.Identifier(DATABASE_NAME)))

        # reconnect to the database and create tables there
        self.connect_to_db()
        cursor = self.conn.cursor()
        cursor.execute(CREATE_TABLES)
