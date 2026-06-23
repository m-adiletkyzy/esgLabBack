from urllib.parse import urlparse

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, User, Permission, Group
from django.core.exceptions import PermissionDenied, ValidationError
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
    Approved = models.BooleanField(default=True)
    added_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)


class Article(Base):
    ar_date = models.DateTimeField()
    ar_site_url = models.URLField(max_length=2000, null=True, blank=True)
    HasOurArticle = models.BooleanField(default=False)
    OurArticleId = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title + ' ' + str(self.OurArticleId)

    class Meta:
        ordering = ['-ar_date']

    def updateOur(self, title, text, instance):
        if title.replace(' ', '') == '' or text.replace(' ', '') == '':
            self.delete()
        else:
            self.image_url = instance.image_url()
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

    def updateOur(self, title, text, instance):
        if title.replace(' ', '') == '' or text.replace(' ', '') == '':
            self.delete()
        else:
            self.image_url = instance.image_url()
            self.title = title
            self.digest = text
            self.isActive = instance.is_active
            self.save()



class Course(Base):
    cr_site_url = models.URLField(max_length=2000)
    isActive = models.BooleanField(default=True)
    HasOurCourse = models.BooleanField(default=False)
    OurCourseId = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title

    def updateOur(self, title, text, instance):
        if title.replace(' ', '') == '' or text.replace(' ', '') == '':
            self.delete()
        else:
            self.image_url = instance.image_url()
            self.title = title
            self.digest = text
            self.isActive = instance.is_active
            self.save()



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

    def updateOur(self, title, text, instance):
        if title.replace(' ', '') == '' or text.replace(' ', '') == '':
            self.delete()
        else:
            self.image_url = instance.image_url()
            self.title = title
            self.digest = text
            self.event_date = instance.date
            self.isActive = instance.is_active
            self.save()

# For objects that need hand filtration

class ToFilter(models.Model):
    esgScore = models.IntegerField()

    class Meta:
        ordering = ['esgScore']
        abstract = True

    def Approve(self):
        self.Approved = True
        self.save()

    def Disapprove(self):
        self.delete()

class ArticleToFilter(Article, ToFilter):
    pass
class CourseToFilter(Course, ToFilter):
    pass
class EventToFilter(Event, ToFilter):
    pass
class ProjectToFilter(Project, ToFilter):
    pass


class OurBase(models.Model):
    Rutitle = models.TextField()
    Rutext = models.TextField()

    Engtitle = models.TextField(null=True, blank=True)
    Engtext = models.TextField(null=True, blank=True)

    Kktitle = models.TextField(null=True, blank=True) # Kaz title
    Kktext = models.TextField(null=True, blank=True) # Kaz text

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        # Ensure that Engtitle and Engtext are either both filled or both blank
        if (self.Engtitle and not self.Engtext) or (not self.Engtitle and self.Engtext):
            raise ValidationError('Both Engtitle and Engtext must either be both filled or both blank.')

        # Ensure that Kktitle and Kktext are either both filled or both blank
        if (self.Kktitle and not self.Kktext) or (not self.Kktitle and self.Kktext):
            raise ValidationError('Both Kktitle and Kktext must either be both filled or both blank.')

        # You can add other validation logic here if needed

        super().clean()  # Call the parent class clean method to ensure any other validation is done


class OurArticle(OurBase):
    image = models.ImageField(upload_to='images/ourarticles/', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Rutitle + ' - ' + str(self.date)

    def image_url(self):
        if self.image:
            return self.image.url
        return ''


class OurEvent(OurBase):
    image = models.ImageField(upload_to='images/ourevents/', null=True, blank=True)
    date = models.DateTimeField()
    location = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.Rutitle + ' - ' + str(self.date)

    def image_url(self):
        if self.image:
            return self.image.url
        return ''

class OurProject(OurBase):
    STATUS_CHOICES = [
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('planned', 'Planned'),
        ('paused', 'Paused'),
        ('cancelled', 'Cancelled'),
    ]

    image = models.ImageField(upload_to='images/ourprojects/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')  # E.g., 'ongoing', 'completed', 'planned', etc.
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.Rutitle + ' - ' + str(self.created_at)

    def image_url(self):
        if self.image:
            return self.image.url
        return ''

class OurCourse(OurBase):
    image = models.ImageField(upload_to='images/ourcourses/', null=True, blank=True, )
    duration = models.IntegerField(verbose_name='Duration in hours')   # Duration in hours
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    instructor = models.CharField(max_length=255)
    is_online = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.Rutitle + ' - ' + str(self.start_date)

    def image_url(self):
        if self.image:
            return self.image.url
        return ''


class OurUrl(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()

    def __str__(self):
        return self.title


# Permission policy models
class Editor(models.Model):
    User = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.User.username


    def save(self, *args, **kwargs):
        if self.User.is_superuser:
            pass

        # Ensure the user is_staff is True by default for Editor roles
        self.User.is_staff = True

        # Get the group you want to assign (replace 'Editor' with the actual group name)
        group = Group.objects.get(name='Editor')

        # Add the user to the group
        self.User.groups.add(group)

        # Save the editor model
        super().save(*args, **kwargs)
        self.User.save()  # Save the user to persist permissions
        print(self.User.groups.all())

class Manager(models.Model):
    User = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.User.username

    def save(self, *args, **kwargs):
        if self.User.is_superuser:
            pass

        # Ensure the user is_staff is True by default for Editor roles
        self.User.is_staff = True

        # Get the group you want to assign (replace 'Editor' with the actual group name)
        group = Group.objects.get(name='Manager')

        # Add the user to the group
        self.User.groups.add(group)

        # Save the editor model
        super().save(*args, **kwargs)
        self.User.save()  # Save the user to persist permissions

class TelegramUser(models.Model):
    Name = models.CharField(max_length=255)
    TelegramID = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.Name

class ParsingError(models.Model):
    ParsedSite = models.URLField()
    ErrorText = models.TextField()
    ErrorDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        parsed_url = urlparse(self.ParsedSite)
        domain = parsed_url.netloc
        date = self.ErrorDate.strftime("%Y-%m-%d %H:%M")
        return domain + ' ' + str(date)

class blacklistLinks(models.Model):
    link = models.URLField()
