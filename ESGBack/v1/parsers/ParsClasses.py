import datetime
from typing import Union

class ParseBase():
    title = ''
    image_url = ''
    site_url = ''
    url = ''
    lang = ''
    digest = ''

class NewsClass(ParseBase):
    date: Union[datetime.datetime, str] = '' # format '%Y-%m-%d %H:%M'

    def getExtra(self, s): # Get info from the article page
        pass

class CourseClass(ParseBase):
    pass

class ProjectClass(ParseBase):
    pass

class EventClass(ParseBase):
    date = ''
    pass

def printParsed(ar_list):
    for a in ar_list:
        print(a.title)
        print(a.digest)
        print(a.site_url)
        print(a.url)
        print(a.lang)
        print(a.image_url)
        print()