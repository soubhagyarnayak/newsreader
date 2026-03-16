from bs4 import BeautifulSoup
import requests
from datetime import date

from feed_fetcher import FeedItem


class ToiOpinionFetcher:
    def get_feeds(self, url):
        feeds_content = requests.get(url)
        content = BeautifulSoup(feeds_content.text, features="lxml")
        headings = content.find_all("h2", class_="media-heading")
        feeds = []
        for heading in headings:
            a = heading.find("a")
            if a is None:
                continue
            title = a.get("title", "")
            link = a.get("href", "")
            feed = FeedItem(
                title=title,
                link=link,
                description=title,
                publication_date=date.today().strftime("%m/%d/%Y"),
                guid=link,
            )
            feeds.append(feed)
        return feeds
