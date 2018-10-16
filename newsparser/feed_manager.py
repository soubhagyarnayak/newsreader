import sqlite3
from sqlite3 import Error

DATABASE_NAME = 'feeds.db'

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
            cursor.execute("INSERT INTO Feeds(URL,Description) VALUES (?,?)",
                           (url,description))
            
    def remove_feed(self,url):
        connection = self._get_connection()
        with connection:
            cursor = connection.cursor()
            #TODO: make it atomic
            cursor.execute(
                "DELETE FROM FeedEntries WHERE FeedId = (SELECT ROWID FROM Feeds WHERE Feeds.URL=?)",
                (url,))
            cursor.execute("DELETE FROM Feeds WHERE Feeds.URL=?",(url,))
            
    def get_feeds(self):
        connection = self._get_connection()
        feeds = []
        with connection:
            cursor = connection.cursor()
            for row in cursor.execute("SELECT ROWID,URL,Description FROM Feeds"):
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
            cursor.execute("CREATE TABLE IF NOT EXISTS Feeds (URL TEXT UNIQUE, Description TEXT);")
            cursor.execute("CREATE TABLE IF NOT EXISTS FeedEntries (Link TEXT UNIQUE, Title TEXT, Description TEXT, GUID TEXT, PubDate TEXT, FeedId INTEGER);")
    
    def _get_connection(self):
        connection = None
        try:
            connection = sqlite3.connect(DATABASE_NAME)
        except Error as e:
            print(e)
        return connection
