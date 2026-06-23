from datetime import datetime
import pytz
import requests
from bs4 import BeautifulSoup
from v1.parsers.ParsClasses import ArticleClass

link = 'https://www.esgtoday.com/category/esg-news/'
urlbase = 'https://www.esgtoday.com/'
headers = {'User-Agent': 'My User Agent 1.0', }


class ESGTodayArticle(ArticleClass):
    def __init__(self, soup, lang, link):
        datetxt = soup.find('time')['datetime']
        date0 = datetime.strptime(datetxt, '%Y-%m-%d')

        self.title = soup.find('h2', {'class': 'post-title entry-title'}).text
        self.url = soup.find('h2', {'class': 'post-title entry-title'}).find('a')['href']
        self.date = pytz.utc.localize(date0, '%Y-%m-%d %H:%M')
        self.image_url = soup.find('img')['src']
        self.site_url = link
        self.lang = lang

    def getExtra(self, s): # Get info from the article page
        try:
            raw = s.get(self.url, headers=headers)
            soup = BeautifulSoup(raw.text, 'lxml')
            print(self.url)
            self.digest = soup.find('div', {'class': 'entry-content'}).find('p').text

        except:
            pass

def ParseEsgToday():
    raw = requests.get(link)
    soup = BeautifulSoup(raw.text, 'lxml')
    ar = soup.find('div', {'class': 'loops-wrapper'})
    ar_soup_list = ar.find_all('article')
    ArtList = [ESGTodayArticle(a, 'en', link) for a in ar_soup_list]

    return ArtList

