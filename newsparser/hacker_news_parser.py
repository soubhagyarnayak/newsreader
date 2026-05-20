import logging
from dataclasses import dataclass

from feed_fetcher import HtmlFetcher
from html_utils import HtmlUtils

HACKER_NEWS_URL = "https://news.ycombinator.com/"

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@dataclass
class HackerNewsArticle:
    id: str
    link: str
    title: str
    tags: str
    content: str

    def __str__(self):
        encoded_title = self.title.encode("utf8")
        return f"{self.id}\t{self.link}\t{encoded_title}"


class HackerNewsParser:
    def parse_all(self):
        url_article_map = self.parse_page(HACKER_NEWS_URL)
        yield url_article_map
        page_id = 2
        while True:
            try:
                logger.info(f"Parsing page with id:{page_id} and length:{len(url_article_map)}")
                page_url_article_map = self.parse_page(f"{HACKER_NEWS_URL}/news?p={page_id}")
                if not page_url_article_map:
                    break  # HN returns empty page at times
                yield page_url_article_map
                page_id += 1
            except Exception:
                break

    def parse_page(self, page_url):
        url_article_map = {}
        fetcher = HtmlFetcher()
        page_content = fetcher.get_raw_content(page_url)
        if not page_content:
            return url_article_map
        articles = page_content.find_all("tr", class_="athing")
        for article in articles:
            article_id = article.get("id")
            titles = article.find_all("td", class_="title")
            for title in titles:
                article_links = title.find_all("a")
                if not article_links:
                    continue
                link = article_links[0].get("href")
                content, tags = HtmlUtils.extract_text_and_keywords_from_url(link)
                url_article_map[link] = HackerNewsArticle(article_id, link, article_links[0].text, tags, content)
        return url_article_map

    def parse_comments(self, article_url):
        pass
