import re
import time

import requests

from v1.parsers.ParsClasses import CourseClass
from bs4 import BeautifulSoup

EyacademyRu = 'https://eyacademycca.com/esg/'



class EyacademyCourse(CourseClass):
    def __init__(self, c, lang, siteUrl):
        self.title = c['title']
        self.digest = re.sub(r'<.*?>', ' ', c['descr']) + '\nЦена: ' + c['editions'][0]['price'][:-5] + 'тг'

        ind = (c['gallery'].find('https'), c['gallery'].find('"}]'))
        self.image_url =  c['gallery'][ind[0]:ind[1]]
        self.url = c['url']
        self.site_url = siteUrl
        self.lang = lang

def Parse_EyacademyBase(link):
    data = requests.get(
        'https://store.tildaapi.pro/api/getproductslist/?storepartuid=818568445401&recid=792018402&c=1741146634084&getparts=true&getoptions=true&slice=1&size=12')

    return data.json()['products']

def Parse_EyacademyRuCourses():
    courses_soup_list = Parse_EyacademyBase(EyacademyRu)
    courses_list = [EyacademyCourse(c, 'ru', EyacademyRu) for c in courses_soup_list]

    return courses_list

