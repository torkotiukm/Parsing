import lxml
import requests 
from bs4 import BeautifulSoup
import sqlite3

URL = "https://scrapingclub.com/exercise/list_basic/?page=1https://scrapingclub.com/exercise/list_basic/?page=1"

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                         'like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'accept': '*/*'
}

HOST = "https://scrapingclub.com"
#фунуція повертає код веб сторінки
def get_html(url):
    response = requests.get(url, HEADERS)
    return response

def get_content(html): #збвр данних
    if html.status_code == 200: #якщр сайт нам відповів
        products = list()
        soup = BeautifulSoup(html.text, "lxml")
        items = soup.find_all("div", class_= "p-4") #находимо потрібні теги
        for item in items: #перебираємо теги 
            if item.find("h4"):
                products.append({ #словник для товару 
                    "Title": item.find("a").text, #записуємо загтловок 
                    "Link": HOST + item.find("a").get("href"), #записуємо посиланнґм на товар
                    "Price": item.find("h5").text[1:] #записуємо ціну 
                })
        return products #повертаємо сптсок товарів 

def savedata(items): #створюємр базу данних і записуємо товари в таблицю
    with sqlite3.connect("products.db") as conn: #відкриваємо базу данних в обєкт
        db = conn.cursor() #створюємо курсор для роботи з бд 
        db.execute("""DELETE FROM clothes""")
        #створюємо таблицю в бд
        db.execute("""CREATE TABLE IF NOT EXISTS clothes( 
                   title TEXT,
                   link TEXT,
                   price INT
        )""")
        conn.commit() #підтвердження змфн в ьазі данних
        for item in items:
            db.execute("""INSERT INTO clothes VALUES(?,?,?)""", [item["Title"], item["Link"], item["Price"]])
        conn.commit()
    


def parse(): 
    prod = list()
    for i in range(1,7): #задаємл кільк сторінок на сайті
        html = get_html(f"https://scrapingclub.com/exercise/list_basic/?page={i}") 
        prod.extend(get_content(html))
        print(f"Parsing {i} page from 6 pages")
    savedata(prod)




parse()