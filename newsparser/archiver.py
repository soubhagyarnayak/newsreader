import os

from feed_fetcher import HtmlFetcher
from custom_fetcher import SamajaFetcher, DharitriFetcher

MAIN_FILE_NAME = "main.html"
SAMAJA_DIR_PATH = "samaja"
DHARITRI_DIR_PATH = "dharitri"


class Archiver:
    def archive_webpage(self, url, directory):
        os.makedirs(directory, exist_ok=True)
        filepath = os.path.join(directory, MAIN_FILE_NAME)
        html_fetcher = HtmlFetcher()
        html_content = html_fetcher.get_raw_content(url)
        with open(filepath, 'w') as file:
            file.write(html_content.prettify())

    def archive_samaja(self, date):
        self._archive(SamajaFetcher(), SAMAJA_DIR_PATH, date)

    def archive_dharitri(self, date):
        self._archive(DharitriFetcher(), DHARITRI_DIR_PATH, date)

    def _archive(self, fetcher, parent_dir_path, date):
        subdir = self.ensure_directory(parent_dir_path, date)
        for page_num, image_content in enumerate(fetcher.fetch(date), start=1):
            filepath = os.path.join(subdir, f"{page_num}.jpg")
            with open(filepath, 'wb') as file:
                file.write(image_content)

    def ensure_directory(self, parent, date):
        os.makedirs(parent, exist_ok=True)
        subdir = os.path.join(parent, date.strftime("%d%m%Y"))
        os.makedirs(subdir, exist_ok=True)
        return subdir


'''archiver = Archiver()
from datetime import datetime, timedelta
archiver.archive_samaja(datetime.now() - timedelta(days=8))
archiver.archive_dharitri(datetime.now() - timedelta(days=8))'''
