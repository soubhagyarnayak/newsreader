import psycopg2

from config import DATABASE_CONFIG

class DatabaseHelper:
    @staticmethod
    def get_connection():
        connection = None
        if DATABASE_CONFIG['type'] == 'postgre':
            user = DATABASE_CONFIG['user']
            password = DATABASE_CONFIG['password']
            dbname = DATABASE_CONFIG['dbname']
            host = DATABASE_CONFIG['host']
            connection = psycopg2.connect("host='{}' dbname='{}' user='{}' password='{}'".format(host,dbname,user,password))
        else:
            raise RuntimeError("The specified db type:{} is not supported".format(DATABASE_CONFIG['type']))
        return connection