import lxml
import requests 
from bs4 import BeautifulSoup
import sqlite3

URL = "https://auto.ria.com/uk/newauto/marka-subaru/"

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                         'like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'accept': '*/*'
}


#фунуція повертає код веб сторінки
def get_html(url, params=None):
    # відправляємо запит на сервер, отримуємо код веб-сторінки
    response = requests.get(url, headers=HEADERS, params=params)
    return response

def get_content(html): #збвр данних
    if html.status_code == 200: #якщр сайт нам відповів
        products = list() #створюємо список 
        soup = BeautifulSoup(html.text, "lxml") 
        items = soup.find_all("div", class_= "proposition_area") #находимо потрібні теги
        for item in items: #перебираємо теги 
            products.append({ #словник для товару 
                "Title": item.find("span", class_= "link").text, #записуємо загтловок 
                "USD": int(item.find("span", class_= "green bold size22").text[4:-6].replace(" ", "")), #записуємо посиланнґм на товар
                "UAH": item.find("span", class_= "size16").text[:-4], #записуємо ціну 
                "City": item.find("span", class_= "item region").text[:-1],
                "Fuel": item.find(lambda tag: tag.name == 'span' and tag.get('class') == ['item']).text.replace("•", "")
            })
        pages = soup.find_all("a", class_= "page-link")
        for page in pages:
            if page.find("a", class_= "page-link"):
                print(page)
        return products #повертаємо сптсок товарів 
    else:
        print(html.status_code)


def parse():
    html = get_html(URL)
    prod1 = get_content(html)
    prod = list()
    prod.extend(prod1)
    #for i in range(1,7): #задаємл кільк сторінок на сайті
     #   html = get_html(f"https://scrapingclub.com/exercise/list_basic/?page={i}") 
      #  prod.extend(get_content(html))
       # print(f"Parsing {i} page from 6 pages")
    #savedata(prod)


parse()

