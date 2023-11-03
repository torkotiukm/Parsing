import lxml
import requests 
from bs4 import BeautifulSoup

URL = "https://scrapingclub.com/exercise/list_basic/?page=1https://scrapingclub.com/exercise/list_basic/?page=1"

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                         'like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'accept': '*/*'
}

HOST = "https://scrapingclub.com"

def get_html(url):
    response = requests.get(url, HEADERS)
    return response

def get_content(html):
    if html.status_code == 200:
        products = list()
        soup = BeautifulSoup(html.text, "lxml")
        items = soup.find_all("div", class_= "p-4")
        for item in items:
            if item.find("h4"):
                products.append({
                    "Title": item.find("a").text, 
                    "Link": HOST + item.find("a").get("href"),
                    "Price": item.find("h5").text[1:]
                })
        print(products)

        

html= get_html(URL)
get_content(html)