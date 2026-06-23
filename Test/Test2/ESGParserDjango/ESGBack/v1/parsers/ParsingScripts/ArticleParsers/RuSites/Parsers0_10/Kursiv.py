from datetime import datetime, timedelta
import pytz
import requests
from bs4 import BeautifulSoup
from v1.parsers.ParsClasses import ArticleClass


link = 'https://kz.kursiv.media/'
base_url = 'https://kz.kursiv.media'
link0 = 'https://kz.kursiv.media/news/page/{n}/'
headers = {'User-Agent': 'My User Agent 1.0', }


class KursivArticle(ArticleClass):
    def __init__(self, soup, lang, link):
        title_classname = 'single-header'
        data = soup.find('div', {'class': title_classname}).find('a')

        self.title = data.text.strip()
        self.digest = soup.find('div', {'class': 'single-body'}).text.strip()
        self.image_url = soup.find('figure').find('img')['data-src']
        self.url = data['href']
        self.date = pytz.utc.localize(datetime.now() - timedelta(days=1))
        self.site_url = link
        self.lang = lang

    def getExtra(self, s): # Get info from the article page
        print(self.url)
        pass

def ParseKursivRu():
    ar_soup_list = []
    for i in range(13):
        raw = requests.get(link0.format(n=i+1), headers=headers)
        soup = BeautifulSoup(raw.text, 'lxml')
        ar = soup.find('div', {'class': 'news-item section-container'})
        ar_soup_list += ar.find_all('article', {'class': 'news-post'})
        ystd_date = datetime.now() - timedelta(days=1)
        ystd = ystd_date.strftime("%Y-%m-%d")


    ArtList = [KursivArticle(a, 'ru', link) for a in ar_soup_list
               if a.find('time')['datetime'][:10] == ystd]

    return ArtList


