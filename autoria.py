import lxml
import requests 
from bs4 import BeautifulSoup
import sqlite3

URL = input("Введи посилання:")
name_table= input("Введи назву таблиці на англ:")

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
                "Title": item.find("span", class_= "link").text[1:-1], #записуємо загтловок 
                "USD": int(item.find("span", class_= "green bold size22").text[4:-6].replace(" ", "")), #записуємо посиланнґм на товар
                "UAH": int(item.find(lambda tag: tag.name == 'span' and tag.get('class') == ['size16']).text[:-4].replace(" ", "")), #записуємо ціну 
                "City": item.find("span", class_= "item region").text[:-1],
                "Fuel": item.find(lambda tag: tag.name == 'span' and tag.get('class') == ['item']).text[1:-1].replace("•", "")
            })
        return products #повертаємо сптсок товарів
    else:
        print(html.status_code)

def pagination(html):
    if html.status_code == 200: #якщр сайт нам відповів
        soup = BeautifulSoup(html.text, "lxml")
        pages = soup.find_all('span', class_='page-item mhide')
        p1 = 1
        for page in pages:
            p = int(page.text)
            if p > p1:
                p1 = p
        return p1
    else:
        print(html.status_code)

def save_data(items):
    with sqlite3.connect("autoria.db") as conn:
        db = conn.cursor()
        db.execute(f"""CREATE TABLE IF NOT EXISTS {name_table}(
                   Title TEXT,
                   USD INT,
                   UAH INT,
                   City TEXT,
                   Fuel TEXT 
        )""")
        db.execute(f"""DELETE FROM {name_table}""")
        for item in items:
            db.execute(f"""INSERT INTO {name_table} VALUES(?,?,?,?,?)""", [item["Title"], item["USD"], item["UAH"], item["City"], item["Fuel"]])
        conn.commit()


def parse():
    html = get_html(URL)
    prod1 = get_content(html)
    prod = list()
    prod.extend(prod1)
    pages = pagination(html)
    print(f"Parsing 1 page from {pages} pages")
    for i in range(2,pages+1): #задаємл кільк сторінок на сайті
       html = get_html(f"https://auto.ria.com/uk/newauto/marka-subaru/?page={i}") 
       prod.extend(get_content(html))
       print(f"Parsing {i} page from {pages} pages")
    save_data(prod)


parse()

