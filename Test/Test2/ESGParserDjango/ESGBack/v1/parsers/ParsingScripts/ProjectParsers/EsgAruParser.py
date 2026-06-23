import requests
import lxml
from bs4 import BeautifulSoup
from v1.parsers.ParsClasses import ProjectClass

link = 'https://esg-a.ru/ru/projects/'
abs_link = 'https://esg-a.ru'


class ESGAruClass(ProjectClass):
    def __init__(self, p:BeautifulSoup, lang, siteUrl):
        self.title = p.find('h4', {'class':'projects__item-title'}).text.strip()
        self.digest = p.find('p', {'class':'content__paragraph'}).text.strip()
        self.lang = lang
        self.site_url = siteUrl
        self.image_url = abs_link + p.find('img')['src']
        self.url = p.find('a', {'class':'readmore-btn'})['href']



def Parse_EsgAruProject():
    raw = requests.get(link)
    soup = BeautifulSoup(raw.text, 'lxml').find('div', {'class': 'projects-page__block'})

    list = soup.find_all('div', {'class': 'projects__item'})
    list = [l for l in list if l.find('a', {'class': 'readmore-btn'})]

    projects = [ESGAruClass(p, 'ru', abs_link) for p in list]

    return projects

