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
            parts = data.split(u'\u0964')  # devnagiri danda aka odia purna cheda
            sentences.extend(parts)
        return [sentence for sentence in sentences if len(sentence) > 0]

    def populate_dictionary(self):
        sentences = self.fetch_random_page_sentences()
        with OdiaDictionary() as odia_dict:
            print(odia_dict.get_stats())
            for sentence in sentences:
                for word in sentence.split():
                    odia_dict.put_meaning_if_missing(word)
            print(odia_dict.get_stats())


# proxy = OdiaWikipediaProxy()
# print(proxy.fetch_random_page().encode("utf-8"))
# proxy.populate_dictionary()
