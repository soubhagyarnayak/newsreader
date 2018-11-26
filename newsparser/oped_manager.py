from oped_store import OpEdStore
from feed_fetcher import RssFeedFetcher

class OpEdManager:
    def process(self):
        oped_store = OpEdStore()
        oped_categories = oped_store.get_categories()
        parser = RssFeedFetcher()
        for oped_category in oped_categories:
            articles = parser.get_feeds(oped_category.link)
            oped_store.add_articles(oped_category,articles)

oped_manager = OpEdManager()
oped_manager.process()