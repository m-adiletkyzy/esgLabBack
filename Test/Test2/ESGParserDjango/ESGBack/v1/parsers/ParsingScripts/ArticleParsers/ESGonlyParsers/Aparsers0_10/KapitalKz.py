import time
from datetime import datetime

import pytz
import requests, lxml
from bs4 import BeautifulSoup

from .v1.parsers.ParsClasses import ArticleClass

kapitalkz = 'https://kapital.kz/'
kapitalkzNews1 = 'https://kapital.kz/info/esg/'
kapitalkzNews2 = 'https://kapital.kz/info/zelenaya-ekonomika-2'

class KapitalkzArticle(ArticleClass):
    def __init__(self, a: BeautifulSoup, lang, siteUrl):
        date0 = a.find('time').text.strip()
        date1 = datetime.strptime(date0, '%d.%m.%Y · %H:%M')
        n = 1
        if a.find_all('a')[n]['href'].count('/') < 2: n = 2
        self.title = a.find_all('a')[n].text
        self.url = 'https://kapital.kz' + a.find_all('a')[n]['href']
        self.digest = a.find('p', {'class':'dh gv dk bd'}).text.strip()
        self.date = pytz.utc.localize(date1)
        self.site_url = siteUrl
        self.lang = lang

    def getExtra(self, s):
        time.sleep(0.5)
        print(self.url)

        headers = {'User-Agent': 'My User Agent 1.0', }
        raw = s.get(self.url, headers=headers)  # Получение страницы ссылки
        soup = BeautifulSoup(raw.text, 'lxml')
        print(soup.prettify())
        soup = soup.find('div', {'class': 'e bn he ef ev bp hf hg hh hi hj hk hl hm hn ho hp hq hr'}).find('figure')

        try:
            self.image_url = soup.find('img')['src']  # Получение картинки
        except Exception as e:
            print(e)
            print('capitalkz image error')


def Parse_KapitalKzBase(link):
    sess = requests.Session()
    headers = {'User-Agent': 'My User Agent 1.0', }
    ar_soup_list = []

    for i in (1, 2, 3):
        raw = sess.get(link + f'?page={i}', headers=headers)
        soup = BeautifulSoup(raw.text, 'lxml').find('div', {'class': 'w em'})
        ar_soup_list += soup.find_all('article', {'class': 'gf gg t e fk gh gi gj gk gl'})

    return ar_soup_list

def Parse_KapitalKzRuNews():
    ar_soup_list = Parse_KapitalKzBase(kapitalkzNews1) + Parse_KapitalKzBase(kapitalkzNews2)
    ar_list = [KapitalkzArticle(a, 'ru', kapitalkz) for a in ar_soup_list if a.find('p', {'class':'dh gv dk bd'})]
    sess = requests.Session()
    for a in ar_list:
        a.getExtra(sess)
    print(len(ar_list))

    return ar_list







