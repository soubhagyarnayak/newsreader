import logging

from dataclasses import dataclass

from database_utils import DatabaseHelper

logger = logging.getLogger(__name__)

PostgreQueries = {
    "create_table": """CREATE TABLE IF NOT EXISTS RSSFeedEntries (
        id SERIAL PRIMARY KEY,
        feed_id INTEGER NOT NULL REFERENCES RSSFeedMetadata(id),
        title TEXT,
        link TEXT UNIQUE,
        description TEXT,
        guid TEXT,
        publication_date TEXT,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    )""",
    "add_entry": """INSERT INTO RSSFeedEntries (feed_id, title, link, description, guid, publication_date)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (link) DO UPDATE SET
            title = excluded.title,
            description = excluded.description,
            guid = excluded.guid,
            publication_date = excluded.publication_date""",
    "get_entries_by_feed_id": "SELECT id, feed_id, title, link, description, guid, publication_date, created_at FROM RSSFeedEntries WHERE feed_id = %s ORDER BY created_at DESC",  # noqa: E501
}


@dataclass
class RSSFeedEntry:
    id: int
    feed_id: int
    title: str
    link: str
    description: str
    guid: str
    publication_date: str
    created_at: str

    def __str__(self):
        return f"id:{self.id},feed_id:{self.feed_id},title:{self.title},link:{self.link}"


def _row_to_entry(row):
    return RSSFeedEntry(
        id=row[0], feed_id=row[1], title=row[2], link=row[3],
        description=row[4], guid=row[5], publication_date=row[6], created_at=row[7]
    )


class RSSFeedStore:
    def create_table_if_absent(self):
        connection = DatabaseHelper.get_connection()
        with connection:
            cursor = connection.cursor()
            cursor.execute(PostgreQueries["create_table"])

    def add_entries(self, feed_id, entries):
        connection = DatabaseHelper.get_connection()
        with connection:
            cursor = connection.cursor()
            for entry in entries:
                cursor.execute(PostgreQueries["add_entry"], (
                    feed_id,
                    entry.title,
                    entry.link,
                    entry.description,
                    entry.guid,
                    entry.publication_date,
                ))
        logger.info(f"Stored {len(entries)} entries for feed_id:{feed_id}")

    def get_entries_by_feed_id(self, feed_id):
        connection = DatabaseHelper.get_connection()
        with connection:
            cursor = connection.cursor()
            cursor.execute(PostgreQueries["get_entries_by_feed_id"], (feed_id,))
            rows = cursor.fetchall()
        return [_row_to_entry(row) for row in rows]
