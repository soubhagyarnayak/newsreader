import wptools
import requests
from bs4 import BeautifulSoup

class OdiaWikipediaProxy:
    def fetch_random_page_paragraphs(self):
        random_page = wptools.page(lang='or')
        random_page_url = random_page.get_query().data['url']
        random_page_content =  requests.get(random_page_url)
        with open('rand101.txt', 'w', encoding='utf-8') as f:
            f.write(random_page_content.text)
        soup = BeautifulSoup(random_page_content.text,'html.parser')
        return soup.find_all('p')

'''proxy = OdiaWikipediaProxy()
#print(proxy.fetch_random_page().encode("utf-8"))
with open('rand102.txt', 'w', encoding='utf-8') as f:
    paragrapghs = proxy.fetch_random_page()
    for paragraph in paragrapghs:
        f.write(paragraph.text)
        f.write("\n\n\n")
'''