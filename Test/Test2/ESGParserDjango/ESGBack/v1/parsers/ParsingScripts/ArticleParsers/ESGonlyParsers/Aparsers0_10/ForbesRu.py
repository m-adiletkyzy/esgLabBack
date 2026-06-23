import time
from datetime import datetime
from urllib.parse import urlparse

import pytz
from v1.parsers.ParsClasses import printParsed

import requests
from bs4 import BeautifulSoup

from v1.parsers.ParsClasses import ArticleClass

forbesRu ='https://www.forbes.ru/'
forbesRuNews = 'https://www.forbes.ru/sustainability/?page='

class ForbesRuArticle(ArticleClass):
    def __init__(self, a: BeautifulSoup, lang, siteUrl):

        if a.find('p', {'class':'XjpMy'}):
            self.title = a.find('p', {'class':'XjpMy'}).text
        else: self.title = a.text

        self.url = 'https://www.forbes.ru' + a['href']
        self.site_url = siteUrl
        self.lang = lang

    def getExtra(self, s):
        if urlparse(forbesRu).netloc == urlparse(self.url).netloc:  # Проверка того, что ссылки ведут на один сайт
            time.sleep(1)
            headers = {'User-Agent': 'My User Agent 1.0', }
            raw = s.get(self.url, headers=headers)  # Получение страницы ссылки
            soup = BeautifulSoup(raw.text, 'lxml')
            print(self.url)

            try:
                # получение первого обзаца
                self.digest = soup.find('strong', {'class':'rTlfZ'}).text
            except: print('ForbesRu digest error')

            try:
                # получение изображения
                self.image_url = soup.find('div', {'class':'H5m9B +GwA8'}).find('img')['src']
            except: print('ForbesRu image error')

            try:
                # получение даты
                date0 = soup.find('time')['datetime'][:19]
                date1 = datetime.strptime(date0, '%Y-%m-%dT%H:%M:%S') #2024-07-17T10:00:00+03:00
                self.date = pytz.utc.localize(date1)
            except: print('ForbesRu date error')

def Parse_ForbesBase(link):
    headers = {'User-Agent': 'My User Agent 1.0', }
    raw = requests.get(link, headers=headers)
    soup = BeautifulSoup(raw.text, 'lxml')
    ar_soup_list = soup.find_all('a', {'class': 'DqnGT'})

    return ar_soup_list

def Parse_ForbesRuNews():
    ar_soup_list = Parse_ForbesBase(forbesRuNews + '1')
    ar_list = [ForbesRuArticle(a, 'ru', forbesRu) for a in ar_soup_list]

    return ar_list

