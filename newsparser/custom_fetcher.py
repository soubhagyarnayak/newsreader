import base64
import datetime
import io
import uuid
from abc import ABC, abstractmethod

import anthropic
import requests
from bs4 import BeautifulSoup
from PIL import Image

from news_image_parser import ImageUtility


class TextExtractor(ABC):
    @abstractmethod
    def extract(self, image: Image.Image) -> str:
        pass


class ClaudeTextExtractor(TextExtractor):
    def __init__(self):
        self._client = anthropic.Anthropic()

    def extract(self, image: Image.Image) -> str:
        buf = io.BytesIO()
        image.save(buf, format="PNG")
        b64 = base64.standard_b64encode(buf.getvalue()).decode()
        response = self._client.messages.create(
            model="claude-opus-4-6",
            max_tokens=4096,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": b64}},
                    {"type": "text", "text": "Extract all text from this newspaper page image."},
                ],
            }],
        )
        return response.content[0].text


class TesseractTextExtractor(TextExtractor):
    def __init__(self, lang="ori"):
        import pytesseract
        self._pytesseract = pytesseract
        self._lang = lang

    def extract(self, image: Image.Image) -> str:
        return self._pytesseract.image_to_string(image, lang=self._lang)


class SamajaFetcher:
    def fetch(self, date):
        print(f"Trying to fetch The Samaja for {date}")
        date_part = date.strftime("%d%m%Y")
        url = "http://www.samajaepaper.in/epaperimages//{}//{}-md-ct-{}.jpg"
        page_num = 1
        while True:
            print(f"trying to fetch page:{page_num}...")
            response = requests.get(url.format(date_part, date_part, page_num))
            if response.status_code == 404:
                break
            yield response.content
            page_num += 1
        print(f"Fetched all the pages of The Samaja for {date}")


class DharitriFetcher:
    def fetch(self, date):
        print(f"Trying to fetch Dharitri for {date}")
        bbsr_edition_url = self.find_bbsr_url(date)
        print(bbsr_edition_url)
        num_pages = self.find_num_pages(bbsr_edition_url)
        for i in range(num_pages):
            response = requests.get(f"{bbsr_edition_url}/page/{i + 1}")
            print_img = BeautifulSoup(response.text, features="lxml").find(id='print_img')
            response = requests.get(print_img['src'])
            yield response.content
        print(f"Fetched all the pages of Dharitri for {date}")

    def find_bbsr_url(self, date):
        archive_url = f"http://dharitriepaper.in/archive/{date.strftime('%Y-%m-%d')}"
        response = requests.get(archive_url)
        content = BeautifulSoup(response.text, features="lxml")
        anchors = content.find_all('a')
        bbsr_hrefs = [anchor['href'] for anchor in anchors if ('bhubaneswar' in anchor['href'] and 'edition' in anchor['href'])]  # noqa: E501
        return "http://dharitriepaper.in" + bbsr_hrefs[0]

    def find_num_pages(self, edition_url):
        response = requests.get(edition_url)
        ddlist_page = BeautifulSoup(response.text, features="lxml").find(id="ddlistPage")
        options = ddlist_page.find_all('option')
        return len(options)


class SambadaFetcher:
    def process(self, date, extractor: TextExtractor = None):
        if extractor is None:
            extractor = ClaudeTextExtractor()
        for img_bytes in self.fetch(date):
            image = Image.open(io.BytesIO(img_bytes))
            trimmed_image = ImageUtility().trim(image, True)

            img_filename = f"{uuid.uuid4()}.png"
            trimmed_image.save(img_filename)
            print(f"Saved trimmed image: {img_filename}")

            text = extractor.extract(trimmed_image)
            print(text)

            text_filename = f"{uuid.uuid4()}.txt"
            with open(text_filename, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"Saved extracted text: {text_filename}")

    def fetch(self, date):
        if isinstance(date, str):
            date = datetime.date.fromisoformat(date)
        print(f"Trying to fetch Sambada for {date}")
        date_part = date.strftime("%d%m%Y")
        url = "https://sambadepaper.com/epaperimages//{}//{}-md-km-{}.jpg"
        page_num = 1
        while True:
            print(f"trying to fetch page:{page_num}...")
            response = requests.get(url.format(date_part, date_part, page_num))
            if response.status_code == 404:
                break
            yield response.content
            page_num += 1
        print(f"Fetched all the pages of Sambada for {date}")
