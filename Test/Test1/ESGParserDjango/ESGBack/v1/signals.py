from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import OurArticle, Article, OurUrl
from .tasks import *


@receiver(post_save, sender=OurArticle)
def create_article(sender, instance, created, **kwargs):
    url = OurUrl.objects.get(title='OurArticleUrl').url
    site_url = OurUrl.objects.get(title='OurSiteUrl').url

    if created:
        if instance.Rutitle != '' and instance.Rutext != '':
            Article.objects.makeOurAr(site_url, url, instance.Rutitle, instance.Rutext, instance, 'ru')

        if instance.Engtitle != '' and instance.Engtext != '':
            Article.objects.makeOurAr(site_url, url, instance.Engtitle, instance.Engtext, instance, 'en')

        if instance.Kktitle != '' and instance.Kktext != '':
            Article.objects.makeOurAr(site_url, url, instance.Kktitle, instance.Kktext, instance, 'kk')
    else:
        ourArs = Article.objects.filter(OurArticleId=instance.id)
        Rtitle = instance.Rutitle
        Rtext = instance.Rutext
        Etitle = instance.Engtitle
        Etext = instance.Engtext
        Ktitle = instance.Kktitle
        Ktext = instance.Kktext

        if ourArs.filter(lang='ru').exists():
            ourArs.get(lang='ru').updateOurAr(Rtitle, Rtext, 'ru')
        else:
            if Rtitle != '' and Rtext != '':
                Article.objects.makeOurAr(site_url, url, instance, 'ru')

        if ourArs.filter(lang='en').exists():
            ourArs.get(lang='en').updateOurAr(Etitle, Etext, 'en')
        else:
            if Etitle != '' and Etext != '':
                Article.objects.makeOurAr(site_url, url, instance, 'en')

        if ourArs.filter(lang='kk').exists():
            ourArs.get(lang='kk').updateOurAr(Ktitle, Ktext, 'kk')

        else:
            if Ktitle != '' and Ktext != '':
                Article.objects.makeOurAr(site_url, url, instance, 'kk')


@receiver(post_delete, sender=OurArticle)
def article_deleted(sender, instance, **kwargs):
    ourArs = Article.objects.filter(OurArticleId=instance.id)
    ourArs.delete()

@receiver(post_save, sender=OurUrl)
def changed_url(sender, instance, created, **kwargs):
    if created:
        pass
    else:
        if instance.title == 'OurArticleUrl':
            change_article_urls.delay(instance.url)
        elif instance.title == 'OurSiteUrl':
            change_site_url.delay(instance.url)



