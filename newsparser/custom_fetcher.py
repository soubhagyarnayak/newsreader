import requests

class SamajaFetcher:
    def fetch(self, date):
        pages = []
        date_part = date.strftime("%d%m%Y")
        url = "http://www.samajaepaper.in/epaperimages//{}//{}-md-ct-{}.jpg"
        page_num = 1
        while True:
            print("tring to fetch page:{}...".format(page_num))
            response = requests.get(url.format(date_part,date_part,page_num))
            if response.status_code == 404:
                break
            pages.append(response.content)
            page_num += 1
        return pages