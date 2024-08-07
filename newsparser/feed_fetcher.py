import logging
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')  # noqa

from bs4 import BeautifulSoup
import requests
import tenacity
from lxml import etree

logger = logging.getLogger(__name__)


class FeedItem:
    def __init__(self):
        self.summary = None
        self.keywords = None

    def __str__(self):
        return "title:{0},description:{1},link:{2}".format(self.title, self.description, self.link)  # noqa: E501


class RssFeedFetcher:
    def get_feeds(self, url):
        feeds_content = requests.get(url)
        xml = etree.XML(feeds_content.content)
        feeds = []
        for item in xml.iter("item"):
            feedItem = FeedItem()
            for element in item:
                if element.tag == "title":
                    feedItem.title = element.text
                elif element.tag == "description":
                    feedItem.description = element.text
                elif element.tag == "guid":
                    feedItem.guid = element.text
                elif element.tag == "pubDate":
                    feedItem.publication_date = element.text
                elif element.tag == "link":
                    feedItem.link = element.text
            feeds.append(feedItem)
        return feeds


class HtmlFetcher:
    def get_paragraphs(self, url):
        response = requests.get(url)
        content = BeautifulSoup(response.text, features="lxml")
        paragraph_texts = []
        for paragraph in content.find_all('p'):
            paragraph_texts.append(paragraph.text)
        return paragraph_texts

    @tenacity.retry(stop=tenacity.stop_after_attempt(5),
                    wait=tenacity.wait_random(min=1, max=5),
                    before_sleep=tenacity.before_sleep_log(logger, logging.INFO))  # noqa: E501
    def get_raw_content(self, url):
        response = requests.get(url)
        logger.info("Fetched {} and got status code:{}".format(url, response.status_code))  # noqa: E501
        if response.status_code != 200:
            raise Exception("Fetched {} and got status code:{}".format(url, response.status_code))  # noqa: E501
        content = BeautifulSoup(response.text, features="lxml")
        return content

    def get_images(self, raw_content):
        image_tags = raw_content.find_all('img')
        image_urls = [image_tag['src'] for image_tag in image_tags]
        image_contents = []
        for image_url in image_urls:
            image_response = requests.get(image_url)
            if (image_response.status_code == 200):
                image_contents.append(image_response.content)
            else:
                logger.info("Failed to retrieve image at:{},got status:{}".format(image_url, image_response.status))  # noqa: E501
        return image_contents
