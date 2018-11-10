from config import DATABASE_CONFIG

PostgreQueries = {
    "create_article_table":"CREATE TABLE IF NOT EXISTS HackerNewsArticles (Id INT PRIMARY KEY, Link TEXT UNIQUE, Title TEXT, Description TEXT, Notes TEXT, IsRead BOOL, IsRemoved BOOL, Tags TEXT, CreateTime TIMESTAMPTZ DEFAULT NOW());",
    "add_article":"INSERT INTO HackerNewsArticles (Id, Link, Title) VALUES (%s,%s,%s) ON CONFLICT (Id) DO UPDATE SET Title = excluded.Title",
    "mark_article_removed": "UPDATE HackerNewsArticles SET IsRemoved = true WHERE Id=%s",
    "purge_removed_articles": "DELETE FROM HackerNewsArticles WHERE IsRemoved=true",
    "get_n_articles":"SELECT TOP %d ARTICLES FROM HackerNewsArticles WHERE !IsRemoved AND !IsRead ORDER BY CreateTime ASC", 
}

class HackerNewsStore:
    def add_article(self,article):
        connection = self._get_connection()
        with connection:
            cursor = connection.cursor()
            cursor.execute(self._get_query('add_article'), (article.id,article.link,article.title))

    def _get_connection(self):
        connection = None
        if DATABASE_CONFIG['type'] == 'postgre':
            import psycopg2
            user = DATABASE_CONFIG['user']
            password = DATABASE_CONFIG['password']
            dbname = DATABASE_CONFIG['dbname']
            connection = psycopg2.connect("dbname='{}' user='{}' password='{}'".format(dbname,user,password))
        else:
            raise RuntimeError("The specified db type:{} is not supported".format(DATABASE_CONFIG['type']))
        return connection

    def _get_query(self,query_id):
        query = None
        if DATABASE_CONFIG['type'] == 'postgre':
            query = PostgreQueries[query_id]
        else:
            raise RuntimeError("The specified db type:{} is not supported".format(DATABASE_CONFIG['type']))
        return query

