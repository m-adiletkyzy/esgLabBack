from ESGBack.celery0 import app
from .models import *
from .parsers.GroupedParsers.AllArticleParsers import Parse_Articles
from .parsers.GroupedParsers.AllCoursesParsers import Parse_Courses
from .parsers.GroupedParsers.AllProjectParsers import Parse_Projects
from .parsers.GroupedParsers.AllEventParsers import Parse_Events

@app.task
def repeat_order_make():
    Parse_Articles()
    Parse_Courses()
    Parse_Projects()
    Parse_Events()

@app.task
def change_article_urls(url):
    OurArticles = Article.objects.filter(HasOurArticle=True)

    for a in OurArticles:
        a.ar_site_url = f'{url}/{a.lang}/{a.OurArticleId}'
        a.save()

@app.task
def change_site_url(url):
    OurArticles = Article.objects.filter(HasOurArticle=True)

    for a in OurArticles:
        a.site_url = url
        a.save()