import os

from feed_fetcher import HtmlFetcher
from custom_fetcher import SamajaFetcher, DharitriFetcher

MAIN_FILE_NAME = "main.html"
SAMAJA_DIR_PATH = "samaja"
DHARITRI_DIR_PATH = "dharitri"

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
        self._archive(SamajaFetcher(),SAMAJA_DIR_PATH,date)

    def archive_dharitri(self,date):
        self._archive(DharitriFetcher(),DHARITRI_DIR_PATH,date)
    
    def _archive(self,fetcher,parent_dir_path,date):
        image_contents = fetcher.fetch(date)
        subdir = self.ensure_directory(parent_dir_path, date)
        page_num = 1
        for image_content in image_contents:
            filepath = os.path.join(subdir,"{}.jpg".format(page_num))
            with open(filepath,'wb') as file:
                file.write(image_content)
            page_num += 1

    def ensure_directory(self,parent,date):
        if not os.path.exists(parent):
            os.makedirs(parent)
        subdir = os.path.join(parent,date.strftime("%d%m%Y"))
        if not os.path.exists(subdir):
            os.makedirs(subdir)
        return subdir

'''archiver = Archiver()
from datetime import datetime
#archiver.archive_samaja(datetime.now())
archiver.archive_dharitri(datetime.now())'''