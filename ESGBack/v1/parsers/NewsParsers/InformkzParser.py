import requests, time, pytz
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from v1.parsers.ESGfilters import filter_esg_items
from v1.parsers.ParsClasses import NewsClass
from datetime import datetime

link = "https://www.inform.kz/category/ekologiya_s2"

class InformKzNews(NewsClass):
    def __init__(self, c: BeautifulSoup, page, lang, siteUrl):
        title_div = c.find('div', class_="catpageCard_title")
        self.title = title_div.text.strip() if title_div else "Без заголовка"
        self.url = "https://www.inform.kz" + c.find('a')['href']
        date_div = c.find('div', class_='catpageCard_time')
        raw_date = date_div.text.strip()
        self.date = self.clean_and_format_date(raw_date)
        self.digest = self.title
        self.page = page
        self.site_url = siteUrl
        self.lang = lang

    def getExtra(self, s):
        if urlparse(link).netloc == urlparse(self.url).netloc:
            time.sleep(0.1)
            print(f"Загрузка {self.url}")
            headers = {'User-Agent': 'My User Agent 1.0'}
            raw = s.get(self.url, headers=headers)
            soup = BeautifulSoup(raw.text, 'lxml')

            try:
                self.image_url = soup.find('figure').find('img', src=True)['src']
            except:
                print('InformKZ image error')

            try:
                article_main = soup.find('div', class_='article__body-main')
                if article_main:
                    h1 = article_main.find('h1', class_='article__title')
                    if h1:
                        self.title = h1.text.strip()
                        self.digest = self.title
            except:
                print('InformKZ digest/title error')


    @staticmethod
    def clean_and_format_date(raw_text):
        time_part, date_part = raw_text.split(", ")
        full_date = f"{date_part} {time_part}"
        # "05 Июнь 2025 19:00"

        # Словарь для русских месяцев
        months = {
            "Январь": "January",
            "Февраль": "February",
            "Март": "March",
            "Апрель": "April",
            "Май": "May",
            "Июнь": "June",
            "Июль": "July",
            "Август": "August",
            "Сентябрь": "September",
            "Октябрь": "October",
            "Ноябрь": "November",
            "Декабрь": "December",
        }

        # Заменяем русское название месяца
        for ru, en in months.items():
            full_date = full_date.replace(ru, en)

        # Теперь парсим
        dt = datetime.strptime(full_date, "%d %B %Y %H:%M")
        return pytz.utc.localize(dt)
        

def Parse_informkzBase(header):
    headers = {'User-Agent': 'My User Agent 1.0'}
    session = requests.Session()
    raw = session.get(link, headers=headers)
    soup = BeautifulSoup(raw.text, 'lxml')

    news_cards = soup.find_all('div', class_="catpageCard")
    return news_cards


def Parse_informkzRuNews(max_pages=5):
    headers = {'User-Agent': 'My User Agent 1.0'}
    session = requests.Session()
    result = []

    for page in range(1, max_pages + 1):
        url = f"https://www.inform.kz/category/ekologiya_s2?page={page}"
        print(f"Парсинг страницы {page}: {url}")
        raw = session.get(url, headers=headers)
        soup = BeautifulSoup(raw.text, 'lxml')

        news_cards = soup.find_all('div', class_="catpageCard")
        if not news_cards:
            print(f"Страница {page} пуста. Прерываем.")
            break

        for card in news_cards:
            news = InformKzNews(card, str(page), 'ru', link)
            result.append(news)

    return filter_esg_items(result, 'ru')
