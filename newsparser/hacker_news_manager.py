from hacker_news_parser import HackerNewsParser
from hacker_news_store import HackerNewsStore

class HackerNewsManager:
    def process(self):
        parser = HackerNewsParser()
        articles = parser.parse_all().values()
        store = HackerNewsStore()
        for article in articles:
            store.add_article(article)

