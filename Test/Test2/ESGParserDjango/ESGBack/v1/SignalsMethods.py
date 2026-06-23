from .models import *

def makeOurAr(s_url, url, title, text, instance, lang):
    Article.objects.create(OurArticleId=instance.id, HasOurArticle=True, title=title,
                           digest=text, image_url=instance.image_url(), site_url=f'{s_url}',
                           lang=lang, ar_site_url=f'{url}/{lang}/{instance.id}', ar_date=instance.date)

def makeOurCr(s_url, url, title, text, instance, lang):
    Course.objects.create(OurCourseId=instance.id, HasOurCourse=True, title=title,
                           digest=text, image_url=instance.image_url(), site_url=f'{s_url}',
                           lang=lang, cr_site_url=f'{url}/{lang}/{instance.id}',
                           isActive=instance.is_active)

def makeOurEv(s_url, url, title, text, instance, lang):
    Event.objects.create(OurEventId=instance.id, HasOurEvent=True, title=title,
                           digest=text, image_url=instance.image_url(), site_url=f'{s_url}',
                           lang=lang, ev_site_url=f'{url}/{lang}/{instance.id}',
                           event_date=instance.date, isActive=instance.is_active)

def makeOurPr(s_url, url, title, text, instance, lang):
    Project.objects.create(OurProjectId=instance.id, HasOurProject=True, title=title,
                           digest=text, image_url=instance.image_url(), site_url=f'{s_url}',
                           lang=lang, pr_site_url=f'{url}/{lang}/{instance.id}',
                           isActive=instance.is_active)
