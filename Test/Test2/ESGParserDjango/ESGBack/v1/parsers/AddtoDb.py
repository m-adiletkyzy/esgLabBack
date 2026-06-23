import datetime

import requests
from v1.parsers.ParsClasses import ArticleClass, ProjectClass, CourseClass, EventClass  #ESGParserDjango.ESGBack.
from v1.models import Article, Project, Course, Event, ArticleToFilter, CourseToFilter, blacklistLinks, ParsingError
from v1.parsers.NlpMethods import KeywordsFiltration
# from v1.parsers.ChatBots import DeepSeek



def addError(site, error):
    ParsingError.objects.create(ParsedSite=site, ErrorText=error)

def AddArticle(ParsedList: list[ArticleClass]):
    if len(ParsedList) > 0:
        site_url = ParsedList[0].site_url
        ArticlesFromSiteinDb = Article.objects.filter(site_url=site_url)

        session = requests.Session()

        for a in ParsedList:
            if not ArticlesFromSiteinDb.filter(ar_site_url=a.url).exists():
                a.getExtra(session)
                create_Article(a)

def AddProjects(ParsedList: list[ProjectClass]):
    if len(ParsedList)>0:
        site_url = ParsedList[0].site_url
        ProjectsFromSiteinDb = Project.objects.filter(site_url=site_url)


        checkActive(ParsedList, ProjectsFromSiteinDb)

        for p in ParsedList:
            if not ProjectsFromSiteinDb.filter(pr_site_url=p.url).exists():
                create_Project(p)
            elif not ProjectsFromSiteinDb.get(pr_site_url=p.url).isActive:
                create_Project(p)


def AddCourses(ParsedList: list[CourseClass]):
    if len(ParsedList) > 0:
        site_url = ParsedList[0].site_url
        CoursesFromSiteinDb = Course.objects.filter(site_url=site_url)

        checkActive(ParsedList, CoursesFromSiteinDb)

        for c in ParsedList:
            if not CoursesFromSiteinDb.filter(cr_site_url=c.url).exists():
                create_Course(c)
            elif not CoursesFromSiteinDb.get(cr_site_url=c.url).isActive:
                create_Course(c)


def AddEvent(ParsedList: list[EventClass]):
    if len(ParsedList) > 0:
        site_url = ParsedList[0].site_url
        EventsFromSiteinDb = Event.objects.filter(site_url=site_url)

        checkActive(ParsedList, EventsFromSiteinDb)

        for e in ParsedList:
            if not EventsFromSiteinDb.filter(ev_site_url=e.url).exists():
                create_Event(e)
            elif not EventsFromSiteinDb.get(ev_site_url=e.url).isActive:
                create_Event(e)

# def AddToFilterArticle(ParsedList: list[ArticleClass], lang):
#     site_url = ParsedList[0].site_url
#     ArticlesFromSiteinDb = ArticleToFilter.objects.filter(site_url=site_url)

#     if len(ParsedList) > 0:
#         # Filtration
#         KwFilter = KeywordsFiltration(lang)
#         KwFilteredParsedList = [a for a in ParsedList if KwFilter.EsgKeyWordCheck(a.title + ' ' + a.digest, lang)]
#         Ai = DeepSeek()
#         session = requests.Session()

#         for a in KwFilteredParsedList:
#             if not ArticlesFromSiteinDb.filter(ar_site_url=a.url).exists():
#                 a.getExtra(session)

#                 try:
#                     EsgScore = int(Ai.ArticleFilter(a.title + '\n' + a.digest))
#                 except:
#                     try:
#                         EsgScore = int(Ai.ArticleFilter(a.title + '\n' + a.digest))
#                     except:
#                         EsgScore = 0

#                 if EsgScore > 8:
#                     create_ArticleToFilter(a, EsgScore, True)
#                 elif EsgScore > 5:
#                     create_ArticleToFilter(a, EsgScore, False)

# def AddToFilterCourses(ParsedList: list[CourseClass]):
#     if len(ParsedList) > 0:
#         site_url = ParsedList[0].site_url
#         CoursesFromSiteinDb = Course.objects.filter(site_url=site_url)
#         checkActive(ParsedList, CoursesFromSiteinDb)
#         blacklist = blacklistLinks.objects.all()
#         Ai = DeepSeek()

#         ParsedList = [c for c in ParsedList if not blacklist.filter(link=c.url).exists()]

#         for c in ParsedList:
#             try:
#                 EsgScore = int(Ai.CourseFilter(c.title + '\n' + c.digest))
#             except:
#                 try:
#                     EsgScore = int(Ai.CourseFilter(c.title + '\n' + c.digest))
#                 except:
#                     EsgScore = 0

#             def CourseEsgFilter(c:CourseClass, EsgScore):
#                 if EsgScore > 8:
#                     create_CourseToFilter(c, EsgScore, True)
#                 elif EsgScore > 5:
#                     create_CourseToFilter(c, EsgScore, False)
#                 else:
#                     addToBlackList(c.url)

#             if not CoursesFromSiteinDb.filter(cr_site_url=c.url).exists():
#                 CourseEsgFilter(c, EsgScore)
#             elif not CoursesFromSiteinDb.get(cr_site_url=c.url).isActive:
#                 CourseEsgFilter(c, EsgScore)


def create_Article(a:ArticleClass):
    Article.objects.create(title=a.title, ar_date=a.date, digest=a.digest,
                                  image_url=a.image_url, site_url=a.site_url, ar_site_url=a.url, lang=a.lang)

def create_Project(p:ProjectClass):
    Project.objects.create(title=p.title, pr_site_url=p.url, site_url=p.site_url,
                           image_url=p.image_url, lang=p.lang, digest=p.digest)

def create_Course(c:CourseClass):
    Course.objects.create(title=c.title, cr_site_url=c.url, site_url=c.site_url,
                           image_url=c.image_url, lang=c.lang, digest=c.digest)

def create_Event(e:EventClass):
    Event.objects.create(title=e.title, ev_site_url=e.url, site_url=e.site_url,
                           image_url=e.image_url, lang=e.lang, digest=e.digest, event_date=e.date)

def create_ArticleToFilter(a:ArticleClass, EsgScore, Approved):
    ArticleToFilter.objects.create(title=a.title, ar_date=a.date, digest=a.digest,
                                  image_url=a.image_url, site_url=a.site_url, ar_site_url=a.url, lang=a.lang,
                                      esgScore=EsgScore, Approved=Approved)
def create_CourseToFilter(c:CourseClass, EsgScore, Approved):
    CourseToFilter.objects.create(title=c.title, cr_site_url=c.url, site_url=c.site_url,
                                  image_url=c.image_url, lang=c.lang, digest=c.digest,
                                  esgScore=EsgScore, Approved=Approved)

def addToBlackList(url):
    blacklistLinks.objects.create(link=url)



# проверка активности (есть ли на сайте этот объект сейчас)
def checkActive(ParsedList: list, DbList: list):
    ParsedList = [obj.url for obj in ParsedList]

    if type(ParsedList[0]) == CourseClass:
        for obj in DbList:
            if obj.cr_site_url not in ParsedList:
                obj.isActive = False
                obj.save()
    elif type(ParsedList[0]) == ProjectClass:
        for obj in DbList:
            if obj.pr_site_url not in ParsedList:
                obj.isActive = False
                obj.save()
    elif type(ParsedList[0]) == EventClass:
        for obj in DbList:
            if obj.ev_site_url not in ParsedList:
                obj.isActive = False
                obj.save()







