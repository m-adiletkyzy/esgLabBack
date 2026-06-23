import requests
from bs4 import BeautifulSoup

from v1.parsers.ParsClasses import CourseClass

CsdCenterKzRu = 'https://csd-center.kz/?lang=ru'

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
    raw = requests.get(link, headers=headers)
    soup = BeautifulSoup(raw.text, 'lxml').find('div', {'class': 'block-trainings'})
    course_soup_list = soup.find_all('div', {'class': 'item-content'})

    return course_soup_list

def Parse_CsdCenterKzRuCourses():
    course_soup_list = Parse_CsdCenterKzCoursesBase(CsdCenterKzRu)
    course_list = [CsdCenterKzCourse(c, 'ru', CsdCenterKzRu) for c in course_soup_list]
    return course_list



