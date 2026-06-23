import datetime

import requests
from v1.parsers.ParsClasses import CourseClass, NewsClass, ProjectClass, EventClass
from v1.models import Course, News, Project, Event

def AddNews(parsed_list: list[NewsClass]):
    if not parsed_list:
        print("ParsedList пустой, пропускаем.")
        return

    site_url = parsed_list[0].site_url
    articles_from_site = News.objects.filter(site_url=site_url)

    session = requests.Session()

    if not articles_from_site.exists():
        print(f"Добавление всех новостей с сайта {site_url}")
        for a in parsed_list:
            try:
                a.getExtra(session)
                create_News(a)
            except Exception as e:
                print(f"Ошибка при добавлении: {a.title} — {e}")
    else:
        try:
            last_date = articles_from_site.latest("ar_date").ar_date
        except Exception as e:
            print(f"Ошибка при получении latest даты: {e}")
            last_date = None

        filtered = []
        for l in parsed_list:
            if isinstance(l.date, datetime.datetime):
                if last_date is None or l.date > last_date:
                    filtered.append(l)
            else:
                print(f"Неверный формат даты у новости: {l.title}")

        print(f"Новых новостей для добавления: {len(filtered)}")

        for a in filtered:
            if not articles_from_site.filter(ar_site_url=a.url).exists():
                try:
                    a.getExtra(session)
                    create_News(a)
                except Exception as e:
                    print(f"Ошибка при добавлении: {a.title} — {e}")


def AddCourse(ParsedList: list[CourseClass]):
    if ParsedList:
        site_url = ParsedList[0].site_url
        CoursesFromSiteinDb = Course.objects.filter(site_url=site_url)

        if not CoursesFromSiteinDb:
            for c in ParsedList:
                create_Course(c)
        else:
            checkActive(ParsedList, CoursesFromSiteinDb)

            for c in ParsedList:
                existing_course = CoursesFromSiteinDb.filter(cr_site_url=c.url).order_by('-pars_date').first()
                if existing_course is None:
                    create_Course(c)
                elif not existing_course.isActive:
                    create_Course(c)

def AddProject(ParsedList: list[ProjectClass]):
    if ParsedList:
        site_url = ParsedList[0].site_url
        ProjectsFromSiteinDb = Project.objects.filter(site_url=site_url)

        if not ProjectsFromSiteinDb:
            for p in ParsedList:
                create_Project(p)
        else:
            checkActive(ParsedList, ProjectsFromSiteinDb)

            for p in ParsedList:
                existing_project = ProjectsFromSiteinDb.filter(pr_site_url=p.url).order_by('-pars_date').first()
                if existing_project is None:
                    create_Project(p)
                elif not existing_project.isActive:
                    create_Project(p)
                    
def AddEvent(ParsedList: list[EventClass]):
    if ParsedList:
        site_url = ParsedList[0].site_url
        EventsFromSiteinDb = Event.objects.filter(site_url=site_url)

        if not EventsFromSiteinDb:
            for c in ParsedList:
                create_Event(c)
        else:
            checkActive(ParsedList, EventsFromSiteinDb)

            for e in ParsedList:
                existing_event = EventsFromSiteinDb.filter(ev_site_url=e.url).order_by('-pars_date').first()
                if existing_event is None:
                    create_Event(e)
                elif not existing_event.isActive:
                    create_Event(e)

def create_News(a:NewsClass):
    News.objects.create(title=a.title, ar_date=a.date, digest=a.digest,
                                  image_url=a.image_url, site_url=a.site_url, ar_site_url=a.url, lang=a.lang)

def create_Course(c:CourseClass):
    Course.objects.create(title=c.title, cr_site_url=c.url, site_url=c.site_url,
                           image_url=c.image_url, lang=c.lang, digest=c.digest)
    
def create_Project(p:ProjectClass):
    Project.objects.create(title=p.title, pr_site_url=p.url, site_url=p.site_url,
                           image_url=p.image_url, lang=p.lang, digest=p.digest)
    
def create_Event(e:EventClass):
    Event.objects.create(title=e.title, ev_site_url=e.url, site_url=e.site_url,
                           image_url=e.image_url, lang=e.lang, digest=e.digest, event_date=e.date)


def checkActive(ParsedList: list, DbList: list):
    if not ParsedList:
        return

    parsed_urls = {obj.url for obj in ParsedList}

    for obj in DbList:
        db_url = None
        if hasattr(obj, 'cr_site_url'):
            db_url = obj.cr_site_url
        elif hasattr(obj, 'pr_site_url'):
            db_url = obj.pr_site_url
        elif hasattr(obj, 'ev_site_url'):
            db_url = obj.ev_site_url

        if db_url and db_url not in parsed_urls and obj.isActive:
            obj.isActive = False
            obj.save(update_fields=['isActive'])
