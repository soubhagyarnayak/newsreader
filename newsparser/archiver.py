import os

from feed_fetcher import HtmlFetcher

MAIN_FILE_NAME = "main.html"

class Archiver:
    def archive_webpage(self,url,directory):
        if not os.path.exists(directory):
            os.makedirs(directory)
        filepath = os.path.join(directory,MAIN_FILE_NAME)
        html_fetcher = HtmlFetcher()
        html_content = html_fetcher.get_raw_content(url)
        with open(filepath,'w') as file:
            file.write(html_content.prettify())
        