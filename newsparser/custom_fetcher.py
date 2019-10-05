import requests
from bs4 import BeautifulSoup

class SamajaFetcher:
    def fetch(self, date):
        print("Trying to fetch The Samaja for {}".format(date))
        date_part = date.strftime("%d%m%Y")
        url = "http://www.samajaepaper.in/epaperimages//{}//{}-md-ct-{}.jpg"
        page_num = 1
        while True:
            print("tring to fetch page:{}...".format(page_num))
            response = requests.get(url.format(date_part,date_part,page_num))
            if response.status_code == 404:
                break
            yield response.content
            page_num += 1
        print("Fetched all the pages of The Samaja for {}".format(date))

class DharitriFetcher:
    def fetch(self, date):
        print("Trying to fetch Dharitri for {}".format(date))
        bbsr_edition_url = self.find_bbsr_url(date)
        print(bbsr_edition_url)
        num_pages = self.find_num_pages(bbsr_edition_url)
        for i in range(num_pages):
            response = requests.get(bbsr_edition_url+"/page/"+str(i+1))
            print_img = BeautifulSoup(response.text,features="lxml").find(id='print_img')
            response = requests.get(print_img['src'])
            yield response.content
        print("Fetched all the pages of Dharitri for {}".format(date))

    def find_bbsr_url(self,date):
        archive_url= "http://dharitriepaper.in/archive/{}".format(date.strftime("%Y-%m-%d"))
        response = requests.get(archive_url)
        content = BeautifulSoup(response.text,features="lxml")
        anchors = content.find_all('a')
        bbsr_hrefs = [anchor['href'] for anchor in anchors if ('bhubaneswar' in anchor['href'] and 'edition' in anchor['href'])]
        return "http://dharitriepaper.in"+bbsr_hrefs[0]
    
    def find_num_pages(self,edition_url):
        response = requests.get(edition_url)
        ddlistPage = BeautifulSoup(response.text,features="lxml").find(id="ddlistPage")
        options = ddlistPage.find_all('option')
        return len(options)

class SambadaFetcher:
    def fetch(self, date):
        pass