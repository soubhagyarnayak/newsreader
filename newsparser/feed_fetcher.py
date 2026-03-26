import logging
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')  # noqa

from dataclasses import dataclass

from bs4 import BeautifulSoup
import requests
import tenacity
from lxml import etree

logger = logging.getLogger(__name__)


@dataclass
class FeedItem:
    title: str = ""
    link: str = ""
    description: str = ""
    guid: str = ""
    publication_date: str = ""
    summary: str | None = None
    keywords: str | None = None

    def __str__(self):
        return f"title:{self.title},description:{self.description},link:{self.link}"


class RssFeedFetcher:
    def get_feeds(self, url):
        feeds_content = requests.get(url)
        xml = etree.XML(feeds_content.content)
        feeds = []
        for item in xml.iter("item"):
            feed_item = FeedItem()
            for element in item:
                if element.tag == "title":
                    feed_item.title = element.text
                elif element.tag == "description":
                    feed_item.description = element.text
                elif element.tag == "guid":
                    feed_item.guid = element.text
                elif element.tag == "pubDate":
                    feed_item.publication_date = element.text
                elif element.tag == "link":
                    feed_item.link = element.text
            feeds.append(feed_item)
        return feeds


class HtmlFetcher:
    def get_paragraphs(self, url):
        response = requests.get(url)
        content = BeautifulSoup(response.text, features="lxml")
        return [p.text for p in content.find_all('p')]

    @tenacity.retry(stop=tenacity.stop_after_attempt(10),
                    wait=tenacity.wait_exponential(multiplier=1, min=2, max=60),
                    before_sleep=tenacity.before_sleep_log(logger, logging.INFO))
    def get_raw_content(self, url):
        response = requests.get(url)
        logger.info(f"Fetched {url} and got status code:{response.status_code}")
        if response.status_code == 404:
            return None
        if response.status_code != 200:
            logger.info(f"Failed to retrieve content at:{url},got headers:{response.headers}")
            raise Exception(f"Fetched {url} and got status code:{response.status_code}")
        return BeautifulSoup(response.text, features="lxml")

    def get_images(self, raw_content):
        image_urls = [tag['src'] for tag in raw_content.find_all('img')]
        image_contents = []
        for image_url in image_urls:
            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                image_contents.append(image_response.content)
            else:
                logger.info(f"Failed to retrieve image at:{image_url},got status:{image_response.status_code}")
        return image_contents
