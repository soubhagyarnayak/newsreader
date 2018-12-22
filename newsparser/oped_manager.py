from tqdm import tqdm
from oped_store import OpEdStore
from feed_fetcher import RssFeedFetcher, HtmlFetcher
from text_analyzer import TextAnalyzer

class OpEdManager:
    def process(self):
        oped_store = OpEdStore()
        oped_categories = oped_store.get_categories()
        parser = RssFeedFetcher()
        html_fetcher = HtmlFetcher()
        text_analyzer = TextAnalyzer()
        for oped_category in tqdm(oped_categories, total=len(oped_categories)):
            try:
                articles = parser.get_feeds(oped_category.link)
                for article in articles:
                    try:
                        paragraphs = html_fetcher.get_paragraphs(article.link)
                        text = ' '.join(paragraphs)
                        article.keywords = text_analyzer.get_keywords(text)
                        article.summary = text_analyzer.get_summary(text)
                    except Exception as e:
                        print("Encountered exception while fetching and processing article.")
                        print(e)
                        break
                oped_store.add_articles(oped_category,articles)
            except Exception as e:
                print("Encountered exception while processing op ed feeds.")
                print(e)
                break
