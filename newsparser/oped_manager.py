import logging

from tqdm import tqdm
from oped_store import OpEdStore
from feed_fetcher import RssFeedFetcher, HtmlFetcher
from text_analyzer import TextAnalyzer
from custom_feed_fetcher import ToiOpinionFetcher

logger = logging.getLogger(__name__)


class OpEdManager:
    def __init__(self):
        self.html_fetcher = HtmlFetcher()
        self.text_analyzer = TextAnalyzer()
        self.oped_store = OpEdStore()

    def process(self):
        oped_categories = self.oped_store.get_categories()
        parser = RssFeedFetcher()
        toi_oped_parser = ToiOpinionFetcher()
        for oped_category in tqdm(oped_categories, total=len(oped_categories)):
            try:
                if oped_category.id == 1:
                    articles = toi_oped_parser.get_feeds('https://timesofindia.indiatimes.com/blogs/')  # noqa: E501
                    self.process_articles(oped_category, articles)
                else:
                    articles = parser.get_feeds(oped_category.link)
                self.process_articles(oped_category, articles)
            except Exception as e:
                logger.exception("Encountered exception while processing op ed feeds for %s", oped_category)

    def process_articles(self, oped_category, articles):
        logger.info(f"Processing {len(articles)} articles for category {oped_category.title}")
        for article in articles:
            try:
                paragraphs = self.html_fetcher.get_paragraphs(article.link)
                text = ' '.join(paragraphs)
                article.keywords = self.text_analyzer.get_keywords(text)
                article.summary = self.text_analyzer.get_summary(text)
            except Exception:
                logger.exception("Encountered exception while fetching and processing article %s", article)
        self.oped_store.add_articles(oped_category, articles)
