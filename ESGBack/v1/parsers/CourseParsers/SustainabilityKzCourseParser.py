import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from v1.parsers.ParsClasses import CourseClass

class SustainabilityKzCourse(CourseClass):
    def __init__(self, c:BeautifulSoup, lang, siteUrl):
        title_class = 'js-store-prod-name js-product-name t-store__card__title t-typography__title t-name t-name_md'
        digest_class = 'js-store-prod-descr t-store__card__descr t-typography__descr t-descr t-descr_xxs'
        self.title = c.find('div', {'class':title_class}).text
        self.digest = c.find('div', {'class':digest_class}).text
        self.image_url = c['data-product-img']
        self.url = c['data-product-url']
        self.site_url = siteUrl
        self.lang = lang


SustainabilityKzRu = 'https://www.sustainability.kz/'

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

def Parse_SustainabilityKzCourseBase(link):
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    except:
        driver = webdriver.Chrome(options=options)

    driver.get(link)


    raw = driver.find_element(By.CLASS_NAME, 't951__cont-wrapper').get_attribute('innerHTML')
    soup = BeautifulSoup(raw, 'lxml')
    time.sleep(5)
    courses = soup.find_all('div', {
        'class': 'js-product t-store__card t-store__stretch-col t-store__stretch-col_100 t-align_center t-item'})
    driver.close()
    return courses

def Parse_SustainabilityKzRuCourse():
    courses = Parse_SustainabilityKzCourseBase(SustainabilityKzRu)
    courses = [SustainabilityKzCourse(c, 'ru', SustainabilityKzRu) for c in courses]


    return courses



#courses = soup.find_all('div', {'class': 'js-product t-store__card t-store__stretch-col t-store__stretch-col_25 t-align_left t-item'})
