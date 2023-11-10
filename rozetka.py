import lxml
import requests 
from bs4 import BeautifulSoup
import sqlite3

URL = "https://rozetka.com.ua/mobile-phones/c80003/"

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                         'like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'accept': '*/*'
}


#фунуція повертає код веб сторінки
def get_html(url, params=None):
    # відправляємо запит на сервер, отримуємо код веб-сторінки
    response = requests.get(url, headers=HEADERS, params=params)
    print(response.status_code)
    return response

def get_content(html): #збвр данних
    if html.status_code == 200: #якщр сайт нам відповів
        products = list()
        soup = BeautifulSoup(html.text, "lxml")
        items = soup.find_all("div", class_= "goods-tile__content") #находимо потрібні теги
        print(items)
        # for item in items: #перебираємо теги 
        #     products.append({ #словник для товару 
        #         "Title": item.find("a").text, #записуємо загтловок 
        #         "Link": HOST + item.find("a").get("href"), #записуємо посиланнґм на товар
        #         "Price": item.find("h5").text[1:] #записуємо ціну 
        #     })
        return products #повертаємо сптсок товарів 
    else:
        print(html.status_code)
get_html(URL)
