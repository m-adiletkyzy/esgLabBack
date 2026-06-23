from django.db.models import Count
from django.shortcuts import render
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from .models import *
from .serializers import *
from .modelFilters import *
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.

class ArticleApiView(generics.ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ArticleFilter

class CourseApiView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CourseFilter


class ProjectApiView(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProjectFilter

class EventApiView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventFilter


#api_view(['GET'])
def getSiteListBase(r, Obj):
    if r.method == 'GET':
        sites = Obj.objects.values('site_url').annotate(count=Count('site_url')).order_by('-count')
        return Response(sites)
@api_view(['GET'])
def getArticleSiteList(request):
   return getSiteListBase(request, Article)

@api_view(['GET'])
def getCourseSiteList(request):
    return getSiteListBase(request, Course)
@api_view(['GET'])
def getEventSiteList(request):
    return getSiteListBase(request, Event)
@api_view(['GET'])
def getProjectSiteList(request):
    return getSiteListBase(request, Project)


