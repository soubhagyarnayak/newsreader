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
        last_updated TIMESTAMP WITH TIME ZONE,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    )""",
    "add_feed": "INSERT INTO RSSFeedMetadata (url, title, description) VALUES (%s, %s, %s) ON CONFLICT (url) DO UPDATE SET title = excluded.title, description = excluded.description",  # noqa: E501
    "get_feed_by_id": "SELECT id, url, title, description, last_updated, created_at FROM RSSFeedMetadata WHERE id = %s",  # noqa: E501
    "get_feed_by_url": "SELECT id, url, title, description, last_updated, created_at FROM RSSFeedMetadata WHERE url = %s",  # noqa: E501
    "get_all_feeds": "SELECT id, url, title, description, last_updated, created_at FROM RSSFeedMetadata ORDER BY created_at ASC",  # noqa: E501
    "update_last_updated": "UPDATE RSSFeedMetadata SET last_updated = NOW() WHERE id = %s",
    "delete_feed": "DELETE FROM RSSFeedMetadata WHERE url = %s",
}


@dataclass
class RSSFeedMetadata:
    id: int
    url: str
    title: str
    description: str
    last_updated: str
    created_at: str

    def __str__(self):
        return f"id:{self.id},url:{self.url},title:{self.title}"


def _row_to_metadata(row):
    return RSSFeedMetadata(
        id=row[0], url=row[1], title=row[2],
        description=row[3], last_updated=row[4], created_at=row[5]
    )


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

    def get_feed_by_id(self, feed_id):
        connection = DatabaseHelper.get_connection()
        with connection:
            cursor = connection.cursor()
            cursor.execute(PostgreQueries["get_feed_by_id"], (feed_id,))
            row = cursor.fetchone()
        return _row_to_metadata(row) if row else None

    def get_feed_by_url(self, url):
        connection = DatabaseHelper.get_connection()
        with connection:
            cursor = connection.cursor()
            cursor.execute(PostgreQueries["get_feed_by_url"], (url,))
            row = cursor.fetchone()
        return _row_to_metadata(row) if row else None

    def get_all_feeds(self):
        connection = DatabaseHelper.get_connection()
        with connection:
            cursor = connection.cursor()
            cursor.execute(PostgreQueries["get_all_feeds"])
            rows = cursor.fetchall()
        return [_row_to_metadata(row) for row in rows]

    def update_last_updated(self, feed_id):
        connection = DatabaseHelper.get_connection()
        with connection:
            cursor = connection.cursor()
            cursor.execute(PostgreQueries["update_last_updated"], (feed_id,))
            logger.info(f"Updated last_updated for feed_id:{feed_id}")

    def delete_feed(self, url):
        connection = DatabaseHelper.get_connection()
        with connection:
            cursor = connection.cursor()
            cursor.execute(PostgreQueries["delete_feed"], (url,))
            logger.info(f"Deleted RSS feed metadata for url:{url}, rows affected:{cursor.rowcount}")
