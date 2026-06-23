from datetime import datetime, timedelta
import pytz
import requests
from bs4 import BeautifulSoup
from .v1.parsers.ParsClasses import ArticleClass


link = 'https://www.inform.kz/'
base_url = 'https://www.inform.kz'
link0 = 'https://www.inform.kz/lenta/?page={page}&start_date={sdate}&end_date={edate}'
headers = {'User-Agent': 'My User Agent 1.0', }


class InformKzArticle(ArticleClass):
    def __init__(self, soup, lang, link):
        self.title = soup.find('div', {'class': 'allNewsCard_title'}).text.strip()
        self.image_url = soup.find('picture').find('source')['srcset']
        self.url = base_url + soup.find('a')['href']
        self.date = pytz.utc.localize(datetime.now() - timedelta(days=1))
        self.site_url = link
        self.lang = lang

    def getExtra(self, s): # Get info from the article page
        print(self.url)
        raw = s.get(self.url, headers=headers)
        soup = BeautifulSoup(raw.text, 'lxml')
        self.digest = soup.find('div', {'class': 'article__description'}).find('p').text

def ParseInformKzRu():
    ar_soup_list = []
    date = datetime.now() - timedelta(days=1)
    str_date = date.strftime("%Y-%m-%d")
    raw = requests.get(link0.format(page=1, sdate=str_date, edate=str_date), headers=headers)
    soup = BeautifulSoup(raw.text, 'lxml')

    i = 1

    while (soup.find('li', {'class': 'page-item active'}).text.strip() == str(i)):
        ar = soup.find('div', {'class': 'allNews__list'})
        ar_soup_list += ar.find_all('div', {'class': 'allNewsCard'})
        i+= 1
        raw = requests.get(link0.format(page=i, sdate=str_date, edate=str_date), headers=headers)
        soup = BeautifulSoup(raw.text, 'lxml')


    ArtList = [InformKzArticle(a, 'ru', link) for a in ar_soup_list]

    return ArtList






