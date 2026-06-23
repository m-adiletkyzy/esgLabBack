from datetime import datetime, timedelta
import pytz
import requests
from bs4 import BeautifulSoup
from v1.parsers.ParsClasses import ArticleClass


link = 'https://tengrinews.kz/'
base_url = 'https://tengrinews.kz'
link0 = 'https://tengrinews.kz/news/page/{n}/'
headers = {'User-Agent': 'My User Agent 1.0', }


class TengriNewsArticle(ArticleClass):
    def __init__(self, soup, lang, link):
        title_classname = 'content_main_item_title'
        data = soup.find('span', {'class': title_classname}).find('a')

        self.title = data.text.strip()
        self.digest = soup.find('span', {'class': 'content_main_item_announce'}).text
        self.image_url = soup.find('picture').find('img')['src']
        self.url = base_url + data['href']
        self.date = pytz.utc.localize(datetime.now() - timedelta(days=1))
        self.site_url = link
        self.lang = lang

    def getExtra(self, s):# Get info from the article page
        print(self.url)
        pass

def ParseTengriNews():
    ar_soup_list = []
    for i in range(4):
        raw = requests.get(link0.format(n=i+1), headers=headers)
        soup = BeautifulSoup(raw.text, 'lxml')
        ar = soup.find('main', {'class': 'container'})
        ar_soup_list += ar.find_all('div', {'class': 'content_main_item'})

    ArtList = [TengriNewsArticle(a, 'ru', link) for a in ar_soup_list
               if a.find('div', {'class': 'content_main_item_meta'}).find('span').text.strip() == 'Вчера']

    return ArtList



