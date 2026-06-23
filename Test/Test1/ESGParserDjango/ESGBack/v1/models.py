from django.core.validators import RegexValidator
from django.db import models
from django.template.defaultfilters import title


# Create your models here.

class Base(models.Model):
    title = models.TextField()
    pars_date = models.DateTimeField(auto_now_add=True)
    digest = models.TextField(null=True, blank=True)
    image_url = models.URLField(null=True, blank=True, max_length=2000)
    site_url = models.URLField()
    lang = models.CharField(max_length=2, validators=[RegexValidator('en|ru|kk')])


class Article(Base):
    ar_date = models.DateTimeField()
    ar_site_url = models.URLField(max_length=2000, null=True, blank=True)
    HasOurArticle = models.BooleanField(default=False)
    OurArticleId = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title + ' ' + str(self.OurArticleId)

    class Meta:
        ordering = ['-ar_date']

    def makeOurAr(self,s_url, url, title, text, instance, lang):
        self.create(OurArticleId=instance.id, HasOurArticle=True, title=title,
                               ar_date=instance.date, digest=text,
                               image_url='http://127.0.0.1:8000/', site_url=f'{s_url}',
                               ar_site_url=f'{url}/{lang}/{instance.id}', lang=lang)

    def updateOurAr(self, title, text, lang):
        self.title = title
        self.digest = text
        self.save()


class Project(Base):
    pr_site_url = models.URLField(max_length=2000)
    isActive = models.BooleanField(default=True)
    HasOurProject = models.BooleanField(default=False)
    OurProjectId = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title



class Course(Base):
    cr_site_url = models.URLField(max_length=2000)
    isActive = models.BooleanField(default=True)
    HasOurCourse = models.BooleanField(default=False)
    OurCourseId = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title

class Event(Base):
    ev_site_url = models.URLField(max_length=2000)
    event_date = models.DateTimeField(null=True, blank=True)
    isActive = models.BooleanField(default=True)

    HasOurEvent = models.BooleanField(default=False)
    OurEventId = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-event_date']


class OurBase(models.Model):
    Rutitle = models.TextField()
    Engtitle = models.TextField(null=True, blank=True)
    Kktitle = models.TextField(null=True, blank=True) # Kaz title

    Rutext = models.TextField()
    Engtext = models.TextField(null=True, blank=True)
    Kktext = models.TextField(null=True, blank=True) # Kaz text


class OurArticle(OurBase):
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Rutitle + ' - ' + str(self.date)


class OurEvent(OurBase):
    date = models.DateTimeField()
    location = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class OurProject(OurBase):
    status = models.CharField(max_length=20)  # E.g., 'ongoing', 'completed', 'planned', etc.
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class OurCourse(OurBase):
    duration = models.IntegerField()  # Duration in hours
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    instructor = models.CharField(max_length=255)
    is_online = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class OurUrl(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()

    def __str__(self):
        return self.title

