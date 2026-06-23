import time

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from v1.parsers.ParsClasses import CourseClass

EyacademyRu = 'https://eyacademycca.com/esg/'
EyacademyKk = 'https://eyacademycca.com/kk/esg/'
EyacademyEn = 'https://eyacademycca.com/en/esg/'

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

class EyacademyCourse(CourseClass):
    def __init__(self, c:BeautifulSoup, lang, siteUrl):
        title_tag = c.find('div', class_=lambda value: value and 'js-store-prod-name' in value)
        descr_tag = c.find('div', class_=lambda value: value and 'js-store-prod-descr' in value)
        price_tag = c.find('div', class_=lambda value: value and 't-store__card__price' in value)

        self.title = title_tag.text.strip() if title_tag else 'No title'

        digest_parts = []
        if descr_tag and descr_tag.text.strip():
            digest_parts.append(descr_tag.text.strip())
        if price_tag and price_tag.text.strip():
            digest_parts.append(price_tag.text.strip())
        self.digest = '\n'.join(digest_parts) if digest_parts else self.title

        self.image_url = c.get('data-product-img', '')
        self.url = c.get('data-product-url', siteUrl)
        self.site_url = siteUrl
        self.lang = lang

def Parse_EyacademyBase(link):
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    except:
        driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(3)
    driver.get(link)
    time.sleep(2)

    try:
        driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(By.CLASS_NAME, 't776'))
        time.sleep(2)
    except NoSuchElementException:
        pass

    raw = driver.page_source

    soup = BeautifulSoup(raw, 'lxml')
    grid = soup.find('div', {'class': 'js-store-grid-cont t-store__grid-cont t-container t-store__grid-cont_mobile-one-row t-store__mobile-two-columns'})
    if not grid:
        grid = soup.find('div', class_=lambda value: value and 'js-store-grid-cont' in value)

    if not grid:
        driver.close()
        return []

    courses_soup_list = grid.find_all(
        'div',
        attrs={
            'data-product-url': True,
            'data-product-img': True,
        },
    )
    driver.close()

    return courses_soup_list

def parse_eyacademy_courses(lang: str, site_url: str):
    courses_soup_list = Parse_EyacademyBase(site_url)
    return [EyacademyCourse(c, lang, site_url) for c in courses_soup_list]


def Parse_EyacademyRuCourses():
    return parse_eyacademy_courses('ru', EyacademyRu)


def Parse_EyacademyKkCourses():
    return parse_eyacademy_courses('kk', EyacademyKk)


def Parse_EyacademyEnCourses():
    return parse_eyacademy_courses('en', EyacademyEn)

