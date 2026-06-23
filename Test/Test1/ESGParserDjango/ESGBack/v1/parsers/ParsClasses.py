import datetime


class ParseBase():
    title = ''
    image_url = ''
    site_url = ''
    url = ''
    lang = ''
    digest = ''


class ArticleClass(ParseBase):
    date: datetime.datetime or str = '' # format '%Y-%m-%d %H:%M'

    def getExtra(self, s): # Get info from the article page
        pass

class ProjectClass(ParseBase):
    pass

class CourseClass(ParseBase):
    pass

class EventClass(ParseBase):
    date = ''
    pass


# For debug

def printParsed(ar_list):
    for a in ar_list:
        print(a.title)
        print(a.digest)
        print(a.site_url)
        print(a.url)
        print(a.lang)
        print(a.image_url)
        print()