import time

import dateutil

from v1.parsers.ParsClasses import ArticleClass
from v1.parsers.ESGfilters import isESGRu
import requests

from bs4 import BeautifulSoup
import lxml
from datetime import datetime
import pytz
from urllib.parse import urlparse



KaseKzRu_url = 'https://kase.kz/ru/'

class KaseKzArticle(ArticleClass):
    def __init__(self, soup: BeautifulSoup, lang, siteUrl):
        datetxt = soup.find('div', {'class': 'news-list__date'}).text.strip()
        date0 = datetime.strptime(datetxt, '%d.%m.%y %H:%M')
        t_soup = soup.find('div', {'class':'news-list__title'})
        urlbase = 'https://kase.kz'

        self.title = t_soup.find('a').text.strip().replace('\n', ' ')
        self.url = urlbase + t_soup.find('a', href=True)['href']  # получение ссылки на статью
        self.date = pytz.utc.localize(date0, '%Y-%m-%d %H:%M')
        self.site_url = siteUrl
        self.lang = lang

    def getExtra(self, s):
        if urlparse(KaseKzRu_url).netloc == urlparse(self.url).netloc:  # Проверка того, что ссылки ведут на один сайт
            time.sleep(0.1)
            headers = {'User-Agent': 'My User Agent 1.0', }
            raw = s.get(self.url, headers=headers)  # Получение страницы ссылки
            soup = BeautifulSoup(raw.text, 'lxml')
            print(self.url)

            try:
                # получение первого обзаца
                self.digest = soup.find('div', {'class':'news-block'}).text.split('\n\n', 1)[0].replace('\n', ' ')
            except: print('KaseKznews digest error')


def formD(date0:datetime):
    return date0.strftime('%d.%m.%Y') + '/'


def Parse_KaseKzNewsBase(link):
    # Новости отображаются по периоду времени, возьмём новости за последние 1 недели
    date2 = datetime.now()
    date1 = date2 - dateutil.relativedelta.relativedelta(weeks=1)
    url = link + 'news/' + formD(date1) + formD(date2)

    headers = {'User-Agent': 'My User Agent 1.0', }
    session = requests.Session()

    raw = session.get(url, headers=headers)  # Получение страницы
    soup = BeautifulSoup(raw.text, 'lxml')
    # Номер последней недели
    last_page = int(soup.find('li', {'class': 'pagination__last'}).find('a')['title'])

    Art_list = []

    # Собрать все новости
    for i in range(last_page):
        time.sleep(0.1)
        print(url + str(i + 1))
        raw = session.get(url + str(i + 1), headers=headers)
        soup = BeautifulSoup(raw.text, 'lxml')
        soup = soup.find('ul', {'class': 'news-list'})
        Art_list0 = soup.find_all('li')
        for a in Art_list0: Art_list.append(a)

    return Art_list

def Parse_KaseKzRuNews():
    Art_list = Parse_KaseKzNewsBase(KaseKzRu_url)

    #Сделать из них экземпляр класса Article
    Art_list = [KaseKzArticle(a, 'ru', KaseKzRu_url) for a in Art_list]
    Art_list = [a for a in Art_list if isESGRu(a.title)]

    #Собрать digest к каждой
    #for a in Art_list: a.getDigest(session) (перенёс в addarticletoDb, чтобы не расходовало зря ресурсы)

    print(len(Art_list))



    #Вывод
    '''for a in Art_list:
        print('title: ', a.title)
        print('ar_url: ', a.ar_url)
        print('site_url: ', a.site_url)
        print('date: ', a.date)
        print('digest: ', a.digest, '\n')
    '''

    return Art_list
