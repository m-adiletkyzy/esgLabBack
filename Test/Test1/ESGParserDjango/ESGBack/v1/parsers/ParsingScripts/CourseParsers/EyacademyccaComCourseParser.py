import time

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from v1.parsers.ParsClasses import CourseClass

EyacademyRu = 'https://eyacademycca.com/esg/'

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

class EyacademyCourse(CourseClass):
    def __init__(self, c:BeautifulSoup, lang, siteUrl):
        self.title = c.find('div', {'class':'js-store-prod-name js-product-name t-store__card__title t-typography__title t-name t-name_md'}).text
        self.digest = c.find('div', {'class': 'js-store-prod-descr t-store__card__descr t-typography__descr t-descr t-descr_xxs'}).text + '\n'
        self.digest += c.find('div', {'class': 't-store__card__price t-store__card__price-item t-name t-name_xs'}).text
        self.image_url =  c['data-product-img']
        self.url = c['data-product-url']
        self.site_url = siteUrl
        self.lang = lang

def Parse_EyacademyBase(link):
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    except:
        driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(3)
    driver.get(link)
    driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(By.CLASS_NAME, 't776'))
    time.sleep(3)

    raw = driver.page_source

    soup = BeautifulSoup(raw, 'lxml').find('div', {'class': 'js-store-grid-cont t-store__grid-cont t-container t-store__grid-cont_mobile-one-row t-store__mobile-two-columns'})
    courses_soup_list = soup.find_all('div', {'class':'js-product t-store__card t-col t-col_4 t-align_left t-item'})
    driver.close()

    return courses_soup_list

def Parse_EyacademyRuCourses():
    courses_soup_list = Parse_EyacademyBase(EyacademyRu)
    courses_list = [EyacademyCourse(c, 'ru', EyacademyRu) for c in courses_soup_list]

    return courses_list

