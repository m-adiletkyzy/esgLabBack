import requests
from bs4 import BeautifulSoup

from ..ParsClasses import CourseClass

link_ru = 'https://csd-center.kz/?lang=ru'
link_kk = 'https://csd-center.kz/?lang=kk'
link_en = 'https://csd-center.kz/?lang=en'

class CsdCenterKzCourse(CourseClass):
    def __init__(self, c:BeautifulSoup, lang, siteUrl):
        self.title = c.find('div', {'class': 'content-title'}).text.strip()
        self.digest = c.find('div', {'class': 'content-info'}).text
        self.image_url = 'https://csd-center.kz' + c.find('div', {'class': 'content-icon'}).find('img')['src']
        self.url = 'https://csd-center.kz' + c.find('div', {'class': 'content-icon'}).find('a')['href']
        self.site_url = siteUrl
        self.lang = lang

def Parse_CsdCenterKzCoursesBase(link):
    headers = {'User-Agent': 'My User Agent 1.0', }
    raw = requests.get(link, headers=headers, timeout=30)
    raw.raise_for_status()
    soup = BeautifulSoup(raw.text, 'lxml')

    training_block = soup.find('div', {'class': 'block-trainings'})
    if not training_block:
        return []

    course_soup_list = training_block.find_all('div', {'class': 'item-content'})

    return course_soup_list

def parse_csd_center_courses(lang: str, site_url: str):
    course_soup_list = Parse_CsdCenterKzCoursesBase(site_url)
    return [CsdCenterKzCourse(c, lang, site_url) for c in course_soup_list]


def Parse_CsdCenterKzRuCourses():
    return parse_csd_center_courses('ru', link_ru)


def Parse_CsdCenterKzKkCourses():
    return parse_csd_center_courses('kk', link_kk)


def Parse_CsdCenterKzEnCourses():
    return parse_csd_center_courses('en', link_en)
