import time

from v1.parsers.ParsClasses import ArticleClass
import requests
from bs4 import BeautifulSoup
import lxml
from datetime import datetime
import pytz
from urllib.parse import urlparse

EsgnewscomRu_link = 'https://esgnews.com/ru/'
EsgnewscomEn_link = 'https://esgnews.com/'

class EsgNewsArticle(ArticleClass):

    def __init__(self, soup: BeautifulSoup, lang, siteUrl):
        self.title = soup.find('a').text.strip().replace('\n', ' ')
        self.url = soup.find('a', href=True)['href']  # получение ссылки на статью
        self.date = pytz.utc.localize(datetime.strptime(soup.find('time')['datetime'], '%Y-%m-%d %H:%M'))
        self.site_url = siteUrl
        self.lang = lang


    def getExtra(self, s):
        if urlparse(EsgnewscomRu_link).netloc == urlparse(self.url).netloc:  # Проверка того, что ссылки ведут на один сайт
            time.sleep(0.1)
            print(self.url)
            headers = {'User-Agent': 'My User Agent 1.0', }
            raw = s.get(self.url, headers=headers)  # Получение страницы ссылки
            soup = BeautifulSoup(raw.text, 'lxml')

            try:
                self.image_url = soup.find('figure').find('img', src=True)['src']  # Получение картинки
            except: print('Esgnews image error')

            try:
                soup = soup.find('div',
                             {'class': 'simple-text tt-content title-droid margin-big tw-text-base tw-leading-relaxed'})
                self.digest = soup.find('p').text.strip()  # получение первого обзаца
            except: print('Esgnews digest error')


def Parse_EsgnewscomNewsBase(link):
    headers = {'User-Agent': 'My User Agent 1.0', }
    session = requests.Session()

    raw = session.get(link, headers=headers)  # Получение страницы
    soup = BeautifulSoup(raw.text, 'lxml')



    # Получает все новости
    list0 = soup.find_all('div',
                          {"class": "tw-flex tw-items-start tw-flex-wrap tw-relative tw-z-0 tw-max-w-3xl -tw-m-2"})

    return list0

# Функция для сортировки по дате
def myFunc(l: EsgNewsArticle):
    return l.date

def MakeUniq(list2:list):
    # Сортирует по дате
    list2.sort(key=myFunc, reverse=True)

    # Удаляет все дублирования
    i = 0
    while i + 1 < len(list2):
        if list2[i].title == list2[i + 1].title:
            list2.pop(i)
        else:
            i += 1

    return list2

def Parse_EsgnewscomRuNews():
    list0 = Parse_EsgnewscomNewsBase(EsgnewscomRu_link)
    list2 = [EsgNewsArticle(l, 'ru', EsgnewscomRu_link) for l in list0]



    # Получает все дайджесты (первый обзац статьи)
    #for l in list2: l.getDigest(session) (перенёс в addarticletoDb, чтобы не расходовало зря ресурсы)

    return list2

def Parse_EsgnewscomEnNews():
    list0 = Parse_EsgnewscomNewsBase(EsgnewscomEn_link)
    list2 = [EsgNewsArticle(l, 'en', EsgnewscomEn_link) for l in list0]

    list2 = MakeUniq(list2)

    return list2





