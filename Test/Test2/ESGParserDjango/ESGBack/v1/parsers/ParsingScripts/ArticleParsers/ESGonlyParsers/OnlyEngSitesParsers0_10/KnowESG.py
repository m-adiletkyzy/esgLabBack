from datetime import datetime
import pytz
import requests
from bs4 import BeautifulSoup
from v1.parsers.ParsClasses import ArticleClass

link = 'https://www.knowesg.com/'
base_url = 'https://www.knowesg.com'
headers = {'User-Agent': 'My User Agent 1.0', }


class KnowESGArticle(ArticleClass):
    def __init__(self, soup, lang, link):
        datetxt = soup.find('time')['datetime']
        date0 = datetime.strptime(datetxt, "%Y-%m-%dT%H:%M%z")
        data_classname = 'text-neutral-10 hover:text-primary-dark text-lg transition-colors duration-100 ease-linear sourceserif line-clamp-2'
        data = soup.find('a', {'class': data_classname})

        self.title = data.text
        self.url = base_url + data['href']
        self.date = date0
        self.site_url = link
        self.lang = lang

    def getExtra(self, s): # Get info from the article page
        try:
            raw = s.get(self.url, headers=headers)
            soup = BeautifulSoup(raw.text, 'lxml').find('article')
            print(self.url)
            self.digest = soup.find('h2').text.strip()
            self.image_url = soup.find('picture').find('img')['data-src']

        except:
            pass

def ParseKnowESG():
    raw = requests.get(link, headers=headers)
    soup = BeautifulSoup(raw.text, 'lxml')
    ar = soup.find('ul', {'class': 'mt-8'})
    ar_soup_list = ar.find_all('li')
    ArtList = [KnowESGArticle(a, 'en', link) for a in ar_soup_list]

    return ArtList



