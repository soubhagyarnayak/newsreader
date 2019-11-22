import logging
from feed_fetcher import HtmlFetcher

HACKER_NEWS_URL = "https://news.ycombinator.com/"

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class HackerNewsArticle:
    def __init__(self,id,link,title):
        self.id = id
        self.link = link
        self.title = title
    def __str__(self):
        return "{}\t{}\t{}".format(self.id,self.link,self.title.encode("utf8"))

class HackerNewsParser:
    def parse_all(self):
        url_article_map = self.parse_page(HACKER_NEWS_URL)
        yield url_article_map
        page_id = 2
        while True:
            logger.info("Parsing page with id:{} and length:{}".format(page_id,len(url_article_map)))
            page_url_article_map = self.parse_page(HACKER_NEWS_URL+"/news?p="+str(page_id))
            if len(page_url_article_map) == 0:
                break
            yield page_url_article_map
            page_id +=1

    def parse_page(self, page_url):
        url_article_map = {}
        fetcher = HtmlFetcher()
        page_content = fetcher.get_raw_content(page_url)
        articles = page_content.find_all("tr",class_="athing")
        for article in articles:
            id = article.get("id")
            titles = article.find_all("td", class_="title")
            for title in titles:
                article_links = title.find_all("a")
                if len(article_links) == 0:
                    continue
                link = article_links[0].get("href")
                url_article_map[link]=HackerNewsArticle(id,link,article_links[0].text)
        return url_article_map
    def parse_comments(self, article_url):
        pass