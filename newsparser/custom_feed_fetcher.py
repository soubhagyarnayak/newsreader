from bs4 import BeautifulSoup
import requests
from datetime import date

from feed_fetcher import FeedItem


class ToiOpinionFetcher:
    def get_feeds(self, url):
        feeds = []
        feeds_content = requests.get(url)
        content = BeautifulSoup(feeds_content.text, features="lxml")
        headings = content.findAll("h2", {"class": "media-heading"})
        for heading in headings:
            a = heading.findAll("a")[0]
            feed = FeedItem()
            feed.title = a.get("title")
            feed.link = a.get("href")
            feed.description = feed.title
            feed.publication_date = date.today().strftime("%m/%d/%Y")
            feed.guid = feed.link
            feeds.append(feed)
        return feeds
