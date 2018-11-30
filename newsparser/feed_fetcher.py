from bs4 import BeautifulSoup
import requests
from lxml import etree

class FeedItem:
    def __init__(self):
        self.summary = None
        self.keywords = None
        
    def __str__(self):
        return "title:{0},description:{1},link:{2}".format(self.title,self.description,self.link)

class RssFeedFetcher:
    def get_feeds(self, url):
        print(url)
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
    def get_paragraphs(self,url):
        response = requests.get(url)
        content = BeautifulSoup(response.text,features="lxml")
        paragraph_texts = []
        for paragraph in content.find_all('p'):
            paragraph_texts.append(paragraph.text)
        return paragraph_texts

    def get_raw_content(self,url):
        response = requests.get(url)
        content = BeautifulSoup(response.text,features="lxml")
        return content