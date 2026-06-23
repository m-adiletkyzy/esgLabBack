from django_filters import rest_framework as filters
from .models import *

class ArticleFilter(filters.FilterSet):
    class Meta:
        model = Article
        fields = ['lang', 'site_url']

class CourseFilter(filters.FilterSet):
    class Meta:
        model = Course
        fields = ['lang', 'site_url']

class ProjectFilter(filters.FilterSet):
    class Meta:
        model = Project
        fields = ['lang', 'site_url']

class EventFilter(filters.FilterSet):
    class Meta:
        model = Event
        fields = ['lang', 'site_url']