import wptools
import requests
from bs4 import BeautifulSoup
import re

from odia_dictionary import OdiaDictionary


class OdiaWikipediaProxy:
    def fetch_random_page_paragraphs(self):
        random_page = wptools.page(lang='or')
        random_page_url = random_page.get_query().data['url']
        random_page_content = requests.get(random_page_url)
        with open('rand103.txt', 'w', encoding='utf-8') as f:
            f.write(random_page_content.text)
        soup = BeautifulSoup(random_page_content.text, 'html.parser')
        return soup.find_all('p')

    def fetch_random_page_sentences(self):
        paragraphs = self.fetch_random_page_paragraphs()
        sentences = []
        for paragraph in paragraphs:
            data = re.sub(r'\([^)]*\)', '', paragraph.text)  # remove anything between () including brackets  # noqa: E501
            data = re.sub(r'\[[^]]*\]', '', data)  # remove anything between [] including brackets  # noqa: E501
            data = data.replace('  ', ' ')
            parts = data.split(u'\u0964')  # devnagiri danda aka odia purna cheda  # noqa: E501
            sentences.extend(parts)
        return [sentence for sentence in sentences if len(sentence) > 0]

    def populate_dictionary(self):
        sentences = self.fetch_random_page_sentences()
        with OdiaDictionary() as odia_dict:
            stats = odia_dict.getStats()
            print(stats)
            for sentence in sentences:
                words = sentence.split()
                for word in words:
                    odia_dict.putMeaningIfMissing(word)
            stats = odia_dict.getStats()
            print(stats)


# proxy = OdiaWikipediaProxy()
# print(proxy.fetch_random_page().encode("utf-8"))
# proxy.populate_dictionary()
