import logging

from dataclasses import dataclass

from database_utils import DatabaseHelper

logger = logging.getLogger(__name__)

PostgreQueries = {
    "create_table": """CREATE TABLE IF NOT EXISTS RSSFeedMetadata (
        id SERIAL PRIMARY KEY,
        url TEXT NOT NULL UNIQUE,
        title TEXT NOT NULL,
        description TEXT,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    )""",
    "add_feed": "INSERT INTO RSSFeedMetadata (url, title, description) VALUES (%s, %s, %s) ON CONFLICT (url) DO UPDATE SET title = excluded.title, description = excluded.description",  # noqa: E501
    "get_feed_by_url": "SELECT id, url, title, description, created_at FROM RSSFeedMetadata WHERE url = %s",  # noqa: E501
    "get_all_feeds": "SELECT id, url, title, description, created_at FROM RSSFeedMetadata ORDER BY created_at ASC",  # noqa: E501
    "delete_feed": "DELETE FROM RSSFeedMetadata WHERE url = %s",
}


@dataclass
class RSSFeedMetadata:
    id: int
    url: str
    title: str
    description: str
    created_at: str

    def __str__(self):
        return f"id:{self.id},url:{self.url},title:{self.title}"


class RSSMetadataStore:
    def create_table_if_absent(self):
        connection = DatabaseHelper.get_connection()
        with connection:
            cursor = connection.cursor()
            cursor.execute(PostgreQueries["create_table"])

    def add_feed(self, url, title, description=None):
        connection = DatabaseHelper.get_connection()
        with connection:
            cursor = connection.cursor()
            cursor.execute(PostgreQueries["add_feed"], (url, title, description))
            logger.info(f"Upserted RSS feed metadata for url:{url}")

    def get_feed_by_url(self, url):
        connection = DatabaseHelper.get_connection()
        with connection:
            cursor = connection.cursor()
            cursor.execute(PostgreQueries["get_feed_by_url"], (url,))
            row = cursor.fetchone()
        if row is None:
            return None
        return RSSFeedMetadata(id=row[0], url=row[1], title=row[2], description=row[3], created_at=row[4])

    def get_all_feeds(self):
        connection = DatabaseHelper.get_connection()
        with connection:
            cursor = connection.cursor()
            cursor.execute(PostgreQueries["get_all_feeds"])
            rows = cursor.fetchall()
        return [RSSFeedMetadata(id=row[0], url=row[1], title=row[2], description=row[3], created_at=row[4]) for row in rows]  # noqa: E501

    def delete_feed(self, url):
        connection = DatabaseHelper.get_connection()
        with connection:
            cursor = connection.cursor()
            cursor.execute(PostgreQueries["delete_feed"], (url,))
            logger.info(f"Deleted RSS feed metadata for url:{url}, rows affected:{cursor.rowcount}")
