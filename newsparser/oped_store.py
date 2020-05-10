from database_utils import DatabaseHelper

PostgreQueries = {
    "create_category_table": "CREATE TABLE IF NOT EXISTS OpEdCategory (Id SERIAL PRIMARY KEY, Link Text UNIQUE, Title TEXT, Description TEXT, CreateTime TIMESTAMPTZ DEFAULT NOW());",  # noqa: E501
    "create_article_table": "CREATE TABLE IF NOT EXISTS OpEdArticle (Id SERIAL PRIMARY KEY, CategoryId INTEGER REFERENCES OpEdCategory(id), Link TEXT UNIQUE, Title TEXT, Description TEXT, Notes TEXT, IsRead BOOL, IsRemoved BOOL, Tags TEXT, PublicationTime TIMESTAMPTZ, CreateTime TIMESTAMPTZ DEFAULT NOW(),KeyWords TEXT, Summary TEXT);",  # noqa: E501
    "add_article": u"INSERT INTO OpEdArticle (CategoryId, Link, Title, Description, PublicationTime,KeyWords,Summary) VALUES (%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (Link) DO UPDATE SET Title = excluded.Title,KeyWords=excluded.KeyWords,Summary=excluded.Summary;",  # noqa: E501
    "mark_article_removed": "UPDATE OpEdArticle SET IsRemoved = true WHERE Id=%s",  # noqa: E501
    "purge_removed_articles": "DELETE FROM OpEdArticle WHERE IsRemoved=true",  # noqa: E501
    "get_n_articles": "SELECT TOP %d ARTICLES FROM OpEdArticle WHERE !IsRemoved AND !IsRead ORDER BY CreateTime ASC",  # noqa: E501
    "get_categories": "SELECT Id,Link,Title,Description FROM OpEdCategory;"  # noqa: E501
}


class Category:
    def __init__(self, id, link, title, description):
        self.id = id
        self.link = link
        self.title = title
        self.description = description


class Article:
    def __init__(self, id, link, title, description):
        self.id = id
        self.link = link
        self.title = title
        self.description = description


class OpEdStore:
    def get_categories(self):
        categories = []
        connection = DatabaseHelper.get_connection()
        with connection:
            cursor = connection.cursor()
            cursor.execute(PostgreQueries['get_categories'])
            rows = cursor.fetchall()
            for row in rows:
                category = Category(row[0], row[1], row[2], row[3])
                categories.append(category)
        return categories

    def add_articles(self, category, articles):
        connection = DatabaseHelper.get_connection()
        with connection:
            cursor = connection.cursor()
            for article in articles:
                cursor.execute(PostgreQueries['add_article'],
                               (category.id, article.link, article.title,
                               article.description, article.publication_date,
                               article.keywords, article.summary))

    def get_articles(self):
        pass

    def mark_article_removed(self):
        pass

    def mark_article_read(self):
        pass

    def purge_removed_articles(self):
        pass

    def annotate_article(self):
        pass
