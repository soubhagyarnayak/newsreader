import psycopg2

from config import DATABASE_CONFIG


class DatabaseHelper:
    @staticmethod
    def get_connection():
        if DATABASE_CONFIG['type'] == 'postgre':
            return psycopg2.connect(
                host=DATABASE_CONFIG['host'],
                dbname=DATABASE_CONFIG['dbname'],
                user=DATABASE_CONFIG['user'],
                password=DATABASE_CONFIG['password'],
            )
        raise RuntimeError(f"The specified db type:{DATABASE_CONFIG['type']} is not supported")
