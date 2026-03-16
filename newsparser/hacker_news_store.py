import logging
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')  # noqa

import datetime
import psycopg2
import tenacity

from config import DATABASE_CONFIG
from database_utils import DatabaseHelper

PostgreQueries = {
    "create_article_table": "CREATE TABLE IF NOT EXISTS HackerNewsArticles (Id INT PRIMARY KEY, Link TEXT UNIQUE, Title TEXT, Description TEXT, Notes TEXT, IsRead BOOL, IsRemoved BOOL, Tags TEXT, CreateTime TIMESTAMPTZ DEFAULT NOW());",  # noqa: E501
    "add_article": "INSERT INTO HackerNewsArticles (Id, Link, Title) VALUES (%s,%s,%s) ON CONFLICT (Id) DO UPDATE SET Title = excluded.Title",  # noqa: E501
    "mark_article_removed": "UPDATE HackerNewsArticles SET IsRemoved = true WHERE Id=%s",  # noqa: E501
    "purge_removed_articles": "DELETE FROM HackerNewsArticles WHERE IsRemoved=true AND CreateTime < %s",  # noqa: E501
    "get_n_articles": "SELECT TOP %d ARTICLES FROM HackerNewsArticles WHERE !IsRemoved AND !IsRead ORDER BY CreateTime ASC",  # noqa: E501
}

logger = logging.getLogger(__name__)


class HackerNewsStore:
    @tenacity.retry(stop=tenacity.stop_after_attempt(5),
                    wait=tenacity.wait_random(min=1, max=2),
                    before_sleep=tenacity.before_sleep_log(logger, logging.DEBUG))
    def add_article(self, article):
        connection = DatabaseHelper.get_connection()
        with connection:
            cursor = connection.cursor()
            try:
                cursor.execute(self._get_query('add_article'),
                               (article.id, article.link, article.title))
            except psycopg2.IntegrityError as e:
                logger.info(e)

    def purge(self):
        connection = DatabaseHelper.get_connection()
        with connection:
            cursor = connection.cursor()
            last_create_time = datetime.date.today() - datetime.timedelta(days=10)
            cursor.execute(self._get_query('purge_removed_articles'), (last_create_time,))
            logger.info(f"deleted rows:{cursor.rowcount}")

    def _get_query(self, query_id):
        if DATABASE_CONFIG['type'] == 'postgre':
            return PostgreQueries[query_id]
        raise RuntimeError(f"The specified db type:{DATABASE_CONFIG['type']} is not supported")
