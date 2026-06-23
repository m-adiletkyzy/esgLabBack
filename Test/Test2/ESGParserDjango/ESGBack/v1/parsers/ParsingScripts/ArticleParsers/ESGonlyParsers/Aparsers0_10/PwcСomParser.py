import time
from datetime import datetime
from v1.parsers.ParsClasses import ArticleClass
import pytz
import lxml
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


class PwComArticle(ArticleClass):

    def __init__(self, a: BeautifulSoup, lang, siteUrl):
        date0 = a.find('time')['datetime']
        date1 = datetime.strptime(date0, '%d/%m/%y')

        self.title = a.find('span', {'class': 'ng-binding'}).text
        self.digest = a.find('p', {'class': 'paragraph ng-binding'}).text
        self.site_url = siteUrl
        self.url = a['href']
        self.date = pytz.utc.localize(date1, '%Y-%m-%d %H:%M')
        self.lang = lang
        self.image_url = 'https://www.pwc.com' + a.find('img', {'class':'img-responsive ng-scope'})['src']



options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

PwComRu = 'https://www.pwc.com/kz/ru/'
PwcComRuNews = 'https://www.pwc.com/kz/ru/services/esg.html'

def Parse_PwcComNewsBase(link):
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    except:
        driver = webdriver.Chrome(options=options)

    driver.implicitly_wait(3)
    driver.get(link)
    time.sleep(3)

    raw = driver.find_element(By.ID,
                              'isoContainer--content-pwc-kz-ru-services-esg-jcr-content-root-container-content-free-container-section-844149289-collection-v2').get_attribute(
        'innerHTML')
    soup = BeautifulSoup(raw, 'lxml')
    ar_soup_list = soup.find_all('a', {'class': 'collection__item-link inheritColor ng-scope'})

    return ar_soup_list

def Parse_PwcComRuNews():
    ar_soup_list = Parse_PwcComNewsBase(PwcComRuNews)
    ar_list = [PwComArticle(a, 'ru', PwComRu) for a in ar_soup_list]

    return ar_list






