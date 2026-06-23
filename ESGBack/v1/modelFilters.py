from django_filters import rest_framework as filters
from .models import *


class NewsFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    digest = filters.CharFilter(field_name='digest', lookup_expr='icontains')
    ar_date_after = filters.DateTimeFilter(field_name='ar_date', lookup_expr='gte')
    ar_date_before = filters.DateTimeFilter(field_name='ar_date', lookup_expr='lte')

    class Meta:
        model = News
        fields = ['lang', 'site_url', 'title', 'digest', 'ar_date_after', 'ar_date_before']


class CourseFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    digest = filters.CharFilter(field_name='digest', lookup_expr='icontains')
    isActive = filters.BooleanFilter(field_name='isActive')

    class Meta:
        model = Course
        fields = ['title', 'lang', 'site_url', 'digest', 'isActive']


class ProjectFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    digest = filters.CharFilter(field_name='digest', lookup_expr='icontains')
    isActive = filters.BooleanFilter(field_name='isActive')

    class Meta:
        model = Project
        fields = ['title', 'lang', 'site_url', 'digest', 'isActive']


class EventFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    digest = filters.CharFilter(field_name='digest', lookup_expr='icontains')
    isActive = filters.BooleanFilter(field_name='isActive')
    event_date_after = filters.DateTimeFilter(field_name='event_date', lookup_expr='gte')
    event_date_before = filters.DateTimeFilter(field_name='event_date', lookup_expr='lte')

    class Meta:
        model = Event
        fields = ['title', 'lang', 'site_url', 'digest', 'isActive', 'event_date_after', 'event_date_before']
