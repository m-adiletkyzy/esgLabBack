import re
import time

import requests
from v1.parsers.ParsClasses import CourseClass

class SustainabilityKzCourse(CourseClass):
    def __init__(self, c, lang, siteUrl):
        self.title = c['title']
        self.digest = re.sub(r'<.*?>', ' ', c['descr']) + '\nЦена: ' + c['editions'][0]['price'][:-5] + 'тг'

        ind = (c['gallery'].find('https'), c['gallery'].find('"}]'))
        self.image_url = c['gallery'][ind[0]:ind[1]]
        self.url = c['url']
        self.site_url = siteUrl
        self.lang = lang


SustainabilityKzRu = 'https://www.sustainability.kz/'


def Parse_SustainabilityKzCourseBase(link):
    data = requests.get(
        'https://store.tildaapi.pro/api/getproductslist/?storepartuid=765479943472&recid=807270251&c=1741148261715&getparts=true&getoptions=true&slice=1&filters[quantity]=y&size=36')
    return data.json()['products']

def Parse_SustainabilityKzRuCourse():
    courses = Parse_SustainabilityKzCourseBase(SustainabilityKzRu)
    courses = [SustainabilityKzCourse(c, 'ru', SustainabilityKzRu) for c in courses]


    return courses


