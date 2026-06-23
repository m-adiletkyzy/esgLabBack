import json
import os
import re

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save, post_delete, pre_save, post_migrate
from django.dispatch import receiver

from .SignalsMethods import *
from .middleware import CurrentUserMiddleware
from .tasks import *

# Article Signals
@receiver(post_save, sender=OurArticle)
def create_article(sender, instance, created, **kwargs):
    url = OurUrl.objects.get(title='OurArticleUrl').url
    site_url = OurUrl.objects.get(title='OurSiteUrl').url

    Rtitle = instance.Rutitle
    RtextFull = re.split(r'\n+', instance.Rutext.strip())
    Rtext = RtextFull[0]
    Etitle = instance.Engtitle
    EtextFull = re.split(r'\n+', instance.Engtext.strip())
    Etext = EtextFull[0]
    Ktitle = instance.Kktitle
    KtextFull = re.split(r'\n+', instance.Kktext.strip())
    Ktext = KtextFull[0]

    if created:
        if instance.Rutitle != '' and instance.Rutext != '':
            # Create Article instance for Russian
            makeOurAr(site_url, url, instance.Rutitle, Rtext, instance, 'ru')

        if instance.Engtitle != '' and instance.Engtext != '':
            # Create Article instance for English
            makeOurAr(site_url, url, instance.Engtitle, Etext, instance, 'en')

        if instance.Kktitle != '' and instance.Kktext != '':
            # Create Article instance for Kazakh
            makeOurAr(site_url, url, instance.Kktitle, Ktext, instance, 'kk')

    else:
        # Handle updates to the existing article
        ourArs = Article.objects.filter(OurArticleId=instance.id)

        # Update Russian article if it exists, otherwise create
        if ourArs.filter(lang='ru').exists():
            article = ourArs.get(lang='ru')
            article.updateOur(Rtitle, Rtext, instance)
        else:
            if Rtitle != '' and Rtext != '':
                makeOurAr(site_url, url, Rtitle, Rtext, instance, 'ru')

        # Update English article if it exists, otherwise create
        if ourArs.filter(lang='en').exists():
            article = ourArs.get(lang='en')
            article.updateOur(Etitle, Etext, instance)
        else:
            if Etitle != '' and Etext != '':
                makeOurAr(site_url, url, Etitle, Etext, instance, 'en')

        # Update Kazakh article if it exists, otherwise create
        if ourArs.filter(lang='kk').exists():
            article = ourArs.get(lang='kk')
            article.updateOur(Ktitle, Ktext, instance)
        else:
            if Ktitle != '' and Ktext != '':
                makeOurAr(site_url, url, Ktitle, Ktext, instance, 'kk')

@receiver(post_delete, sender=OurArticle)
def article_delete(sender, instance, **kwargs):
    ourArs = Article.objects.filter(OurArticleId=instance.id)
    ourArs.delete()

# Course Signals
@receiver(post_save, sender=OurCourse)
def create_course(sender, instance, created, **kwargs):
    url = OurUrl.objects.get(title='OurCourseUrl').url
    site_url = OurUrl.objects.get(title='OurSiteUrl').url

    Rtitle = instance.Rutitle
    RtextFull = re.split(r'\n+', instance.Rutext.strip())
    Rtext = RtextFull[0]
    Etitle = instance.Engtitle
    EtextFull = re.split(r'\n+', instance.Engtext.strip())
    Etext = EtextFull[0]
    Ktitle = instance.Kktitle
    KtextFull = re.split(r'\n+', instance.Kktext.strip())
    Ktext = KtextFull[0]

    if created:
        if instance.Rutitle != '' and instance.Rutext != '':
            # Create Сourse instance for Russian
            makeOurCr(site_url, url, instance.Rutitle, Rtext, instance, 'ru')

        if instance.Engtitle != '' and instance.Engtext != '':
            # Create Сourse instance for English
            makeOurCr(site_url, url, instance.Engtitle, Etext, instance, 'en')

        if instance.Kktitle != '' and instance.Kktext != '':
            # Create Сourse instance for Kazakh
            makeOurCr(site_url, url, instance.Kktitle, Ktext, instance, 'kk')

    else:
        # Handle updates to the existing сourse
        ourCrs = Course.objects.filter(OurCourseId=instance.id)

        # Update Russian courses if it exists, otherwise create
        if ourCrs.filter(lang='ru').exists():
            article = ourCrs.get(lang='ru')
            article.updateOur(Rtitle, Rtext, instance)
        else:
            if Rtitle != '' and Rtext != '':
                makeOurCr(site_url, url, Rtitle, Rtext, instance, 'ru')

        # Update English сourses if it exists, otherwise create
        if ourCrs.filter(lang='en').exists():
            article = ourCrs.get(lang='en')
            article.updateOur(Rtitle, Rtext, instance)
        else:
            if Etitle != '' and Etext != '':
                makeOurCr(site_url, url, Etitle, Etext, instance, 'en')

        # Update Kazakh сourses if it exists, otherwise create
        if ourCrs.filter(lang='kk').exists():
            article = ourCrs.get(lang='kk')
            article.updateOur(Rtitle, Rtext, instance)
        else:
            if Ktitle != '' and Ktext != '':
                makeOurCr(site_url, url, Ktitle, Ktext, instance, 'kk')

@receiver(post_delete, sender=OurCourse)
def course_delete(sender, instance, **kwargs):
    ourCrs= Course.objects.filter(OurCourseId=instance.id)
    ourCrs.delete()


# Event Signals

@receiver(post_save, sender=OurEvent)
def create_event(sender, instance, created, **kwargs):
    url = OurUrl.objects.get(title='OurEventUrl').url
    site_url = OurUrl.objects.get(title='OurSiteUrl').url

    Rtitle = instance.Rutitle
    RtextFull = re.split(r'\n+', instance.Rutext.strip())
    Rtext = RtextFull[0]
    Etitle = instance.Engtitle
    EtextFull = re.split(r'\n+', instance.Engtext.strip())
    Etext = EtextFull[0]
    Ktitle = instance.Kktitle
    KtextFull = re.split(r'\n+', instance.Kktext.strip())
    Ktext = KtextFull[0]

    if created:
        if instance.Rutitle != '' and instance.Rutext != '':
            # Create Event instance for Russian
            makeOurEv(site_url, url, instance.Rutitle, Rtext, instance, 'ru')

        if instance.Engtitle != '' and instance.Engtext != '':
            # Create Event instance for English
            makeOurEv(site_url, url, instance.Engtitle, Etext, instance, 'en')

        if instance.Kktitle != '' and instance.Kktext != '':
            # Create Event instance for Kazakh
            makeOurEv(site_url, url, instance.Kktitle, Ktext, instance, 'kk')

    else:
        # Handle updates to the existing event
        ourEvs = Event.objects.filter(OurEventId=instance.id)

        # Update Russian event if it exists, otherwise create
        if ourEvs.filter(lang='ru').exists():
            event = ourEvs.get(lang='ru')
            event.updateOur(Rtitle, Rtext, instance)
        else:
            if Rtitle != '' and Rtext != '':
                makeOurEv(site_url, url, Rtitle, Rtext, instance, 'ru')

        # Update English event if it exists, otherwise create
        if ourEvs.filter(lang='en').exists():
            event = ourEvs.get(lang='en')
            event.updateOur(Etitle, Etext, instance)
        else:
            if Etitle != '' and Etext != '':
                makeOurEv(site_url, url, Etitle, Etext, instance, 'en')

        # Update Kazakh event if it exists, otherwise create
        if ourEvs.filter(lang='kk').exists():
            article = ourEvs.get(lang='kk')
            article.updateOur(Ktitle, Ktext, instance)
        else:
            if Ktitle != '' and Ktext != '':
                makeOurEv(site_url, url, Ktitle, Ktext, instance, 'kk')

@receiver(post_delete, sender=OurEvent)
def course_delete(sender, instance, **kwargs):
    ourEvs= Event.objects.filter(OurEventId=instance.id)
    ourEvs.delete()

@receiver(post_save, sender=OurProject)
def create_project(sender, instance, created, **kwargs):
    url = OurUrl.objects.get(title='OurProjectUrl').url
    site_url = OurUrl.objects.get(title='OurSiteUrl').url

    Rtitle = instance.Rutitle
    RtextFull = re.split(r'\n+', instance.Rutext.strip())
    Rtext = RtextFull[0]
    Etitle = instance.Engtitle
    EtextFull = re.split(r'\n+', instance.Engtext.strip())
    Etext = EtextFull[0]
    Ktitle = instance.Kktitle
    KtextFull = re.split(r'\n+', instance.Kktext.strip())
    Ktext = KtextFull[0]

    if created:
        if instance.Rutitle != '' and instance.Rutext != '':
            # Create Project instance for Russian
            makeOurPr(site_url, url, instance.Rutitle, Rtext, instance, 'ru')

        if instance.Engtitle != '' and instance.Engtext != '':
            # Create Project instance for English
            makeOurPr(site_url, url, instance.Engtitle, Etext, instance, 'en')

        if instance.Kktitle != '' and instance.Kktext != '':
            # Create Project instance for Kazakh
            makeOurPr(site_url, url, instance.Kktitle, Ktext, instance, 'kk')

    else:
        # Handle updates to the existing project
        ourPrs = Project.objects.filter(OurProjectId=instance.id)

        # Update Russian project if it exists, otherwise create
        if ourPrs.filter(lang='ru').exists():
            project = ourPrs.get(lang='ru')
            project.updateOur(Rtitle, Rtext, instance)
        else:
            if Rtitle != '' and Rtext != '':
                makeOurPr(site_url, url, Rtitle, Rtext, instance, 'ru')

        # Update English project if it exists, otherwise create
        if ourPrs.filter(lang='en').exists():
            project = ourPrs.get(lang='en')
            project.updateOur(Etitle, Etext, instance)
        else:
            if Etitle != '' and Etext != '':
                makeOurPr(site_url, url, Etitle, Etext, instance, 'en')

        if ourPrs.filter(lang='kk').exists():
            project = ourPrs.get(lang='kk')
            project.updateOur(instance.Kktitle, Ktext, instance)
        else:
            if Ktitle != '' and Ktext != '':
                makeOurPr(site_url, url, instance.Kktitle, Ktext, instance, 'kk')

@receiver(post_delete, sender=OurProject)
def project_delete(sender, instance, **kwargs):
    ourPrs= Project.objects.filter(OurProjectId=instance.id)
    ourPrs.delete()

@receiver(post_save, sender=OurUrl)
def changed_url(sender, instance, created, **kwargs):
    if created:
        pass
    else:
        if instance.title == 'OurArticleUrl':
            change_article_urls.delay(instance.url)
        elif instance.title == 'OurEventUrl':
            change_event_urls.delay(instance.url)
        elif instance.title == 'OurCourseUrl':
            change_course_urls.delay(instance.url)
        elif instance.title == 'OurProjectUrl':
            change_project_urls.delay(instance.url)
        elif instance.title == 'OurSiteUrl':
            change_site_url.delay(instance.url)


# Permission signals
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import Permission, Group


# Signal handler for ACL policy pre_delete
@receiver(pre_delete, sender=Editor)
def remove_permissions_on_delete(sender, instance, **kwargs):
    # Check if the associated User is not superuser
    if instance.User.is_superuser:
        return

    instance.User.groups.remove(Group.objects.get(name='Editor'))

    # Save the user to persist the changes to the permissions
    if not Manager.objects.filter(User=instance.User).exists():
        instance.User.is_staff = False

    instance.User.save()

@receiver(pre_delete, sender=Manager)
def remove_permissions_on_delete(sender, instance, **kwargs):
    # Check if the associated User is not superuser
    if instance.User.is_superuser:
        return

    instance.User.groups.remove(Group.objects.get(name='Manager'))

    if not Editor.objects.filter(User=instance.User).exists():
        instance.User.is_staff = False

    # Save the user to persist the changes to the permissions
    instance.User.save()

@receiver(pre_delete, sender=User)
def prevent_superuser_delete(sender, instance, **kwargs):
    if instance.is_superuser and not CurrentUserMiddleware.get_current_user().is_superuser:
        raise PermissionDenied("Superuser cannot be deleted.")

# Signal handler for ACL policy pre_save edited
@receiver(pre_save, sender=Editor)
def remove_permissions_on_Editor_save(sender, instance, **kwargs):


    # Check if the associated User is not superuser
    if instance.pk is None or instance.User.is_superuser:
        pass
    else:
        instance0 = Editor.objects.get(pk=instance.pk)
        instance0.User.groups.remove(Group.objects.get(name='Editor'))

        # Save the user to persist the changes to the permissions
        if not Manager.objects.filter(User=instance0.User).exists():
            instance0.User.is_staff = False

        instance0.User.save()

@receiver(pre_save, sender=Manager)
def remove_permissions_on_Manager_save(sender, instance, **kwargs):
    # Check if the associated User is not superuser
    if instance.pk is None or instance.User.is_superuser:
        pass
    else:
        instance0 = Manager.objects.get(pk=instance.pk)
        instance0.User.groups.remove(Group.objects.get(name='Manager'))

        # Save the user to persist the changes to the permissions
        if not Editor.objects.filter(User=instance0.User).exists():
            instance0.User.is_staff = False

        instance0.User.save()


# Initial database datas
@receiver(post_migrate)
def load_initial_data(sender, **kwargs):
    # Вставка данных после применения миграции
    if not OurUrl.objects.exists():
        urls = os.path.join(settings.BASE_DIR, 'InitialData', 'OurUrls', 'Urls.json')
        with open(urls, 'r') as file:
            data = json.load(file)

        OurUrl.objects.create(title='OurSiteUrl', url=data['OurSiteUrl'])
        OurUrl.objects.create(title='OurArticleUrl', url=data['OurArticlesUrl'])
        OurUrl.objects.create(title='OurProjectUrl', url=data['OurProjectUrl'])
        OurUrl.objects.create(title='OurCourseUrl', url=data['OurCourseUrl'])
        OurUrl.objects.create(title='OurEventUrl', url=data['OurEventUrl'])

    '''if not Group.objects.filter(name='Editor').exists():
        # If the group doesn't exist, create it
        group = Group.objects.create(name='Editor')

        # Define the permissions to be added to the group
        permissions = [
            "add_project",
            "change_project",
            "delete_project",
            "view_project",

            "add_event",
            "change_event",
            "delete_event",
            "view_event",

            "add_course",
            "change_course",
            "delete_course",
            "view_course",

            "add_article",
            "change_article",
            "delete_article",
            "view_article",

            "add_ourproject",
            "change_ourproject",
            "delete_ourproject",
            "view_ourproject",

            "add_ourevent",
            "change_ourevent",
            "delete_ourevent",
            "view_ourevent",

            "add_ourcourse",
            "change_ourcourse",
            "delete_ourcourse",
            "view_ourcourse",

            "add_ourarticle",
            "change_ourarticle",
            "delete_ourarticle",
            "view_ourarticle"
        ]

        # Add the permissions to the group
        for permission in permissions:
            permission_obj, _ = Permission.objects.get_or_create(codename=permission)
            group.permissions.add(permission_obj)'''

    if not Group.objects.filter(name='Editor').exists():
        group = Group.objects.create(name='Editor')

        model_map = {
            Project: ["add_project", "change_project", "delete_project", "view_project"],
            Event: ["add_event", "change_event", "delete_event", "view_event"],
            Course: ["add_course", "change_course", "delete_course", "view_course"],
            Article: ["add_article", "change_article", "delete_article", "view_article"],
            OurProject: ["add_ourproject", "change_ourproject", "delete_ourproject", "view_ourproject"],
            OurEvent: ["add_ourevent", "change_ourevent", "delete_ourevent", "view_ourevent"],
            OurCourse: ["add_ourcourse", "change_ourcourse", "delete_ourcourse", "view_ourcourse"],
            OurArticle: ["add_ourarticle", "change_ourarticle", "delete_ourarticle", "view_ourarticle"],
        }

        for model, codenames in model_map.items():
            content_type = ContentType.objects.get_for_model(model)
            for codename in codenames:
                try:
                    permission = Permission.objects.get(codename=codename, content_type=content_type)
                    group.permissions.add(permission)
                except Permission.DoesNotExist:
                    print(f"Permission {codename} does not exist. Run `migrate` first.")

    '''if not Group.objects.filter(name='Manager').exists():
        # If the group doesn't exist, create it
        group = Group.objects.create(name='Manager')

        # Define the permissions to be added to the group
        # List of permission codenames and corresponding field names in Editor model
        permissions = [
            "add_oururl",
            "change_oururl",
            "delete_oururl",
            "view_oururl",

            "add_editor",
            "change_editor",
            "delete_editor",
            "view_editor",

            "add_user",
            "delete_user",
            "view_user",
        ]

        # Add the permissions to the group
        for permission in permissions:
            permission_obj, _ = Permission.objects.get_or_create(codename=permission)
            group.permissions.add(permission_obj)'''

    if not Group.objects.filter(name='Manager').exists():
        group = Group.objects.create(name='Manager')

        model_map = {
            OurUrl: ["add_oururl", "change_oururl", "delete_oururl", "view_oururl"],
            Editor: ["add_editor", "change_editor", "delete_editor", "view_editor"],
            User: ["add_user", "delete_user", "view_user"],  # `User` из `auth`
        }

        for model, codenames in model_map.items():
            content_type = ContentType.objects.get_for_model(model)
            for codename in codenames:
                try:
                    permission = Permission.objects.get(codename=codename, content_type=content_type)
                    group.permissions.add(permission)
                except Permission.DoesNotExist:
                    print(f"Permission {codename} does not exist yet. Run migrations first.")

