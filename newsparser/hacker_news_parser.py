from bs4 import BeautifulSoup
import requests

HACKER_NEWS_URL = "https://news.ycombinator.com/"

class HackerNewsArticle:
    def __init__(self,id,link,title):
        self.id = id
        self.link = link
        self.title = title
    def __str__(self):
        return "{}\t{}\t{}".format(self.id,self.link,self.title.encode("utf8"))

class HackerNewsParser:
    def parse_all(self):
        pass
    def parse_page(self, page_url):
        url_article_map = {}
        response = requests.get(page_url)
        page_content = BeautifulSoup(response.text,features="lxml")
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

'''hnparser = HackerNewsParser()
d = hnparser.parse_page(HACKER_NEWS_URL)
for e in d:
    print(d[e])'''