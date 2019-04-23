import wptools
import requests
from bs4 import BeautifulSoup
import re

class OdiaWikipediaProxy:
    def fetch_random_page_paragraphs(self):
        random_page = wptools.page(lang='or')
        random_page_url = random_page.get_query().data['url']
        random_page_content =  requests.get(random_page_url)
        with open('rand103.txt', 'w', encoding='utf-8') as f:
            f.write(random_page_content.text)
        soup = BeautifulSoup(random_page_content.text,'html.parser')
        return soup.find_all('p')
    
    def fetch_random_page_sentences(self):
        paragraphs = self.fetch_random_page_paragraphs()
        sentences = []
        for paragraph in paragraphs:
            data = re.sub(r'\([^)]*\)', '', paragraph.text) # remove anything between () including brackets
            data = re.sub(r'\[[^]]*\]', '', data) # remove anything between [] including brackets
            data = data.replace('  ',' ')
            parts = data.split(u'\u0964') # devnagiri danda aka odia purna cheda
            sentences.extend(parts)
        return sentences

'''proxy = OdiaWikipediaProxy()
#print(proxy.fetch_random_page().encode("utf-8"))
with open('rand104.txt', 'w', encoding='utf-8') as f:
    sentences = proxy.fetch_random_page_sentences()
    for sentence in sentences:
        f.write(sentence)
        f.write("\n")
'''