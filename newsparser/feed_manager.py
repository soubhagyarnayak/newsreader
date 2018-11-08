import sqlite3
from sqlite3 import Error

import newsparser.config as config

SqliteQueries = {
    'add_feed':'INSERT INTO Feeds(URL,Description) VALUES (?,?)',
    'get_feeds':'SELECT ROWID,URL,Description FROM Feeds',
    'create_feeds_table':'CREATE TABLE IF NOT EXISTS Feeds (URL TEXT UNIQUE, Description TEXT);',
    'create_feed_entries_table': 'CREATE TABLE IF NOT EXISTS FeedEntries (Link TEXT UNIQUE, Title TEXT, Description TEXT, GUID TEXT, PubDate TEXT, FeedId INTEGER);',
    'delete_feed_entries' : 'DELETE FROM FeedEntries WHERE FeedId = (SELECT ROWID FROM Feeds WHERE Feeds.URL=?)',
    'delete_feeds':'DELETE FROM Feeds WHERE Feeds.URL=?'
}

PostgreQueries = {
    'add_feed':'INSERT INTO Feeds(URL,Description) VALUES (%s,%s)',
    'get_feeds': 'SELECT ROWID,URL,Description FROM Feeds',
    'create_feeds_table':'CREATE TABLE IF NOT EXISTS Feeds (ROWID SERIAL, URL TEXT UNIQUE, Description TEXT);',
    'create_feed_entries_table': 'CREATE TABLE IF NOT EXISTS FeedEntries (ROWID SERIAL, Link TEXT UNIQUE, Title TEXT, Description TEXT, GUID TEXT, PubDate TEXT, FeedId INTEGER);',
    'delete_feed_entries' : 'DELETE FROM FeedEntries WHERE FeedId = (SELECT ROWID FROM Feeds WHERE Feeds.URL=%s)',
    'delete_feeds':'DELETE FROM Feeds WHERE Feeds.URL=%s'
}


class Feed:
    def __str__(self):
        return "rowid:{0},url:{1},description:{2}".format(self.id,self.url,self.description)

class FeedEntry:
    pass

class FeedManager:
    
    def add_feed(self,url,description):
        connection = self._get_connection()
        with connection:
            cursor = connection.cursor()
            cursor.execute(self._get_query('add_feed'), (url,description))
            
    def remove_feed(self,url):
        connection = self._get_connection()
        with connection:
            cursor = connection.cursor()
            #TODO: make it atomic
            cursor.execute(
                self._get_query('delete_feed_entries'),(url,))
            cursor.execute(self._get_query('delete_feeds'),(url,))
            
    def get_feeds(self):
        connection = self._get_connection()
        feeds = []
        with connection:
            cursor = connection.cursor()
            cursor.execute("SELECT ROWID,URL,Description FROM Feeds")
            while True:
                row = cursor.fetchone()
                if row == None:
                    break
                feed = Feed()
                feed.id = row[0]
                feed.url = row[1]
                feed.description = row[2]
                feeds.append(feed)
        return feeds
            
    
    def add_entries_to_feed(self,feed_id, entries):
        pass

    def get_feed_entries(self,feed_id, entries):
        pass
    
    def create_tables_if_absent(self):
        connection = self._get_connection()
        with connection:
            cursor = connection.cursor()
            cursor.execute(self._get_query('create_feeds_table'))
            cursor.execute(self._get_query('create_feed_entries_table'))
    
    def _get_connection(self):
        connection = None
        try:
            if config.DATABASE_CONFIG['type'] == 'sqlite':
                connection = sqlite3.connect(config.DATABASE_CONFIG['dbname'])
            elif config.DATABASE_CONFIG['type'] == 'postgre':
                import psycopg2
                user = config.DATABASE_CONFIG['user']
                password = config.DATABASE_CONFIG['password']
                dbname = config.DATABASE_CONFIG['dbname']
                connection = psycopg2.connect("dbname='{}' user='{}' password='{}'".format(dbname,user,password))
            else:
                raise RuntimeError("The specified db type:{} is not supported".format(config.DATABASE_CONFIG['type']))
        except Error as e:
            print(e)
        return connection
    
    def _get_query(self,query_id):
        query = None
        try:
            if config.DATABASE_CONFIG['type'] == 'sqlite':
                query = SqliteQueries[query_id]
            elif config.DATABASE_CONFIG['type'] == 'postgre':
                query = PostgreQueries[query_id]
            else:
                raise RuntimeError("The specified db type:{} is not supported".format(config.DATABASE_CONFIG['type']))
        except Error as e:
            print(e)
        return query
