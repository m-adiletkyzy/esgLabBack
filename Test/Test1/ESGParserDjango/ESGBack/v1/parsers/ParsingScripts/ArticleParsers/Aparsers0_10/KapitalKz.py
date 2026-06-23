import time
from datetime import datetime

import pytz
import requests, lxml
from bs4 import BeautifulSoup

from v1.parsers.ParsClasses import ArticleClass
from v1.parsers.ParsClasses import printParsed

kapitalkz = 'https://kapital.kz/'
kapitalkzNews1 = 'https://kapital.kz/info/esg/'
kapitalkzNews2 = 'https://kapital.kz/info/zelenaya-ekonomika-2'

class KapitalkzArticle(ArticleClass):
    def __init__(self, a: BeautifulSoup, lang, siteUrl):
        date0 = a.find('time')['datetime']
        date1 = datetime.strptime(date0, '%d.%m.%Y · %H:%M')

        self.title = a.find('a', {'class':'main-news__name'}).text
        self.url = 'https://kapital.kz' + a.find('a', {'class':'main-news__name'})['href']
        self.digest = a.find('p', {'class':'main-news__anons'}).text
        self.date = pytz.utc.localize(date1)
        self.site_url = siteUrl
        self.lang = lang

    def getExtra(self, s):
        time.sleep(0.1)
        print(self.url)

        headers = {'User-Agent': 'My User Agent 1.0', }
        raw = s.get(self.url, headers=headers)  # Получение страницы ссылки
        soup = BeautifulSoup(raw.text, 'lxml')

        try:
            self.image_url = soup.find('img', {'class':'lazyload'})['data-src']  # Получение картинки
        except:
            print('capitalkz image error')


def Parse_KapitalKzBase(link):
    sess = requests.Session()
    headers = {'User-Agent': 'My User Agent 1.0', }
    ar_soup_list = []

    for i in (1, 2, 3):
        raw = sess.get(link + f'?page={i}', headers=headers)
        soup = BeautifulSoup(raw.text, 'lxml').find('div', {'class': 'main-news'})
        ar_soup_list += soup.find_all('article', {'class': 'main-news__item'})

    return ar_soup_list

def Parse_KapitalKzRuNews():
    ar_soup_list = Parse_KapitalKzBase(kapitalkzNews1) + Parse_KapitalKzBase(kapitalkzNews2)
    ar_list = [KapitalkzArticle(a, 'ru', kapitalkz) for a in ar_soup_list]

    print(len(ar_list))

    return ar_list





