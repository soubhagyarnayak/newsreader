from hacker_news_parser import HackerNewsParser
from hacker_news_store import HackerNewsStore


class HackerNewsManager:
    def process(self):
        parser = HackerNewsParser()
        store = HackerNewsStore()
        parsed_content = parser.parse_all()
        for article_map in parsed_content:
            for article in article_map.values():
                store.add_article(article)

    def purge(self):
        store = HackerNewsStore()
        store.purge()
