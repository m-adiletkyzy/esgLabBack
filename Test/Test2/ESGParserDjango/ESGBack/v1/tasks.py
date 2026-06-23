from ESGBack.celery0 import app
from .models import *
from .parsers.GroupedParsers.AllArticleParsers import Parse_Articles, Parse_ToFilterArticlesRu
from .parsers.GroupedParsers.AllCoursesParsers import Parse_Courses, Parse_ToFilterCoursesRu
from .parsers.GroupedParsers.AllProjectParsers import Parse_Projects
from .parsers.GroupedParsers.AllEventParsers import Parse_Events

@app.task
def parse_websites():
    ParsingError.objects.all().delete()

    Parse_Articles()
    Parse_Courses()
    Parse_Projects()
    Parse_Events()

    #Parse_ToFilterArticlesRu()
    #Parse_ToFilterCoursesRu()

@app.task
def parse_test():
    Parse_Events()

@app.task
def change_article_urls(url):
    OurArticles = Article.objects.filter(HasOurArticle=True)

    for a in OurArticles:
        a.ar_site_url = f'{url}/{a.lang}/{a.OurArticleId}'
        a.save()

@app.task
def change_event_urls(url):
    OurEvents = Event.objects.filter(HasOurEvent=True)

    for a in OurEvents:
        a.ev_site_url = f'{url}/{a.lang}/{a.OurEventId}'
        a.save()

@app.task
def change_project_urls(url):
    OurProjects = Project.objects.filter(HasOurProject=True)

    for a in OurProjects:
        a.pr_site_url = f'{url}/{a.lang}/{a.OurProjectId}'
        a.save()

@app.task
def change_course_urls(url):
    OurCourses = Course.objects.filter(HasOurCourse=True)

    for a in OurCourses:
        a.cr_site_url = f'{url}/{a.lang}/{a.OurCourseId}'
        a.save()

@app.task
def change_site_url(url):
    OurArticles = Article.objects.filter(HasOurArticle=True)

    for a in OurArticles:
        a.site_url = url
        a.save()

