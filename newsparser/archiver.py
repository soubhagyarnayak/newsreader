import os

from feed_fetcher import HtmlFetcher
from custom_fetcher import SamajaFetcher

MAIN_FILE_NAME = "main.html"
SAMAJA_DIR_PATH = "samaja"

class Archiver:
    def archive_webpage(self,url,directory):
        if not os.path.exists(directory):
            os.makedirs(directory)
        filepath = os.path.join(directory,MAIN_FILE_NAME)
        html_fetcher = HtmlFetcher()
        html_content = html_fetcher.get_raw_content(url)
        with open(filepath,'w') as file:
            file.write(html_content.prettify())
    def archive_samaja(self,date):
        samaja_fetcher = SamajaFetcher()
        image_contents = samaja_fetcher.fetch(date)
        if not os.path.exists(SAMAJA_DIR_PATH):
            os.makedirs(SAMAJA_DIR_PATH)
        subdir = os.path.join(SAMAJA_DIR_PATH,date.strftime("%d%m%Y"))
        if not os.path.exists(subdir):
            os.makedirs(subdir)
        page_num = 1
        for image_content in image_contents:
            filepath = os.path.join(subdir,"{}.jpg".format(page_num))
            with open(filepath,'wb') as file:
                file.write(image_content)
            page_num += 1
'''archiver = Archiver()
from datetime import datetime
archiver.archive_samaja(datetime.now())'''
        