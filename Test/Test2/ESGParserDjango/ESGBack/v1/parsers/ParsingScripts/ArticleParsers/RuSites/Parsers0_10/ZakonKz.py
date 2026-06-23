from datetime import datetime, timedelta

import pytz
import requests
from bs4 import BeautifulSoup

from v1.parsers.ParsClasses import ArticleClass

link = "https://www.zakon.kz"
api = 'https://www.zakon.kz/api/today-news/?pn={page}&pSize=20'
headers = {'User-Agent': 'My User Agent 1.0', }


class ZakonKzArticle(ArticleClass):
    def __init__(self, json, lang, link):
        self.title = json['page_title']
        self.url = link + '/' + json['alias']
        self.date = pytz.utc.localize(datetime.now() - timedelta(days=1))
        self.site_url = link
        self.lang = lang

    def getExtra(self, s): # Get info from the article page
        print(self.url)
        raw = s.get(self.url, headers=headers)
        soup = BeautifulSoup(raw.text, 'lxml')
        article = soup.find('div', {'class': 'article__content'})
        self.image_url = article.find('img', {'class': 'lazy'})['src']
        self.digest = article.find('div', {'class': 'description'}).text.strip()


def ParseZakonKz():
    ar_soup_list = []
    for i in range(4, 14):
        raw = requests.get(api.format(page=i), headers=headers)
        ar_soup_list += raw.json()['data_list']

    ystd = datetime.now() - timedelta(days=1)

    ArtList = [ZakonKzArticle(a, 'ru', link) for a in ar_soup_list
               if a["published_date"][:10] == ystd.strftime('%Y-%m-%d')]

    return ArtList

'''
a = ParseZakonKz()
s = requests.session()
for i in a:
    i.getExtra(s)

for i in a:
    print('title:', i.title)
    print('digest:', i.digest)
    print('site_url:', i.site_url)
    print('url:', i.url)
    print('lang:', i.lang)
    print('image_url:', i.image_url)
    print('date:', i.date)
    print()
'''




