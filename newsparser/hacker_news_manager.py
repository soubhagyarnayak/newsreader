from hacker_news_parser import HackerNewsParser
from hacker_news_store import HackerNewsStore


class HackerNewsManager:
    def process(self):
        parser = HackerNewsParser()
        store = HackerNewsStore()
        parsedContent = parser.parse_all()
        for content in parsedContent:
            articles = content.values()
            for article in articles:
                store.add_article(article)

    def purge(self):
        store = HackerNewsStore()
        store.purge()
