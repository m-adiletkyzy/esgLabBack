import requests
from bs4 import BeautifulSoup

from v1.parsers.ParsClasses import CourseClass

link = 'https://stepik.org/'
url0 = 'https://stepik.org/api/search-results?is_popular=true&is_public=true&language=ru&order=conversion_rate__none,rating__none,quality__none,paid_weight__none,search_boost__none&page={n}&query=esg&type=course'
url1 = 'https://stepik.org/api/courses?'

class StepicCourse(CourseClass):
    def __init__(self, c, lang, siteUrl):
        self.title = c['title']
        self.digest = BeautifulSoup(c['summary'], 'lxml').text.strip() + '\nЦена: '
        if c['price']:
            self.digest += c['display_price']
        else:
            self.digest += 'бесплатно'

        self.image_url = c['cover']
        self.url = c['canonical_url']
        self.site_url = siteUrl
        self.lang = lang


def Parse_StepicCourses():
    course_json_list = []
    for i in range(1, 4):
        raw = requests.get(url0.format(n=i)).json()['search-results']
        url2 = url1
        for i in raw:
            url2 += f'ids[]={i['target_id']}&'
        course_json_list += requests.get(url2[:-1]).json()['courses']

    CourseList = [StepicCourse(c, 'ru', link) for c in course_json_list]


    return CourseList




