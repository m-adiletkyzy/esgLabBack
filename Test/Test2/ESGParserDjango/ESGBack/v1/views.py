import datetime

from django.db.models import Count
from django.shortcuts import render
from rest_framework.decorators import action, api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import *
from .serializers import *
from .modelFilters import *
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.

class ArticleApiView(generics.ListAPIView):
    queryset = Article.objects.filter(Approved=True)
    serializer_class = ArticleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ArticleFilter

class RecentArticleApiView(generics.ListAPIView):
    queryset = Article.objects.filter(Approved=True, added_date=datetime.datetime.now().date() - datetime.timedelta(days=1))
    serializer_class = ArticleSerializer
    pagination_class = None

class RecentOurArticlesApiView(generics.ListAPIView):
    queryset = Article.objects.filter(Approved=True, HasOurArticle=True, added_date__gte=datetime.datetime.now() - datetime.timedelta(hours=5))
    serializer_class = ArticleSerializer
    pagination_class = None

class CourseApiView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CourseFilter

class RecentOurСoursesApiView(generics.ListAPIView):
    queryset = Course.objects.filter(Approved=True, HasOurCourse=True, added_date__gte=datetime.datetime.now() - datetime.timedelta(hours=5))
    serializer_class = CourseSerializer
    pagination_class = None


class ProjectApiView(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProjectFilter

class RecentOurProjectsApiView(generics.ListAPIView):
    queryset = Project.objects.filter(Approved=True, HasOurProject=True, added_date__gte=datetime.datetime.now() - datetime.timedelta(hours=5))
    serializer_class = ProjectSerializer
    pagination_class = None


class EventApiView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventFilter

class RecentOurEventsApiView(generics.ListAPIView):
    queryset = Event.objects.filter(Approved=True, HasOurEvent=True, added_date__gte=datetime.datetime.now() - datetime.timedelta(hours=5))
    serializer_class = EventSerializer
    pagination_class = None


class OurArticleApiView(generics.RetrieveAPIView):
    queryset = OurArticle.objects.all()
    serializer_class = OurArticleSerializer
    lookup_field = 'id'

class OurCourseApiView(generics.RetrieveAPIView):
    queryset = OurCourse.objects.all()
    serializer_class = OurCourseSerializer
    lookup_field = 'id'

class OurProjectApiView(generics.RetrieveAPIView):
    queryset = OurProject.objects.all()
    serializer_class = OurProjectSerializer
    lookup_field = 'id'

class OurEventApiView(generics.RetrieveAPIView):
    queryset = OurEvent.objects.all()
    serializer_class = OurEventSerializer
    lookup_field = 'id'


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

# Telegram bot api
class Pagination1perPage(PageNumberPagination):
    page_size = 1

class ArticlesToFilterApiView(generics.ListAPIView):
    queryset = ArticleToFilter.objects.filter(Approved=False)
    serializer_class = ArticlesToFilterSerializer
    pagination_class = Pagination1perPage

class Pagination5perPage(PageNumberPagination):
    page_size = 5

class getRecentParsingErrors(generics.ListAPIView):
    queryset = ParsingError.objects.all()
    serializer_class = ErrorSerializer
    pagination_class = Pagination5perPage

class ParsingErrorDetailView(generics.RetrieveAPIView):
    queryset = ParsingError.objects.all()
    serializer_class = ErrorSerializer

@api_view(['Post'])
def AproveArticle(request, id):
    ArticleToFilter.objects.get(id=id).Approve()
    return Response({'message': 'Approved'})

@api_view(['Delete'])
def DisapproveArticle(request, id):
    ArticleToFilter.objects.get(id=id).Disapprove()
    return Response({'message': 'Disapproved'})

@api_view(['Post'])
def ApproveCourse(request, id):
    CourseToFilter.objects.get(id=id).Approve()
    return Response({'message': 'Approved'})

@api_view(['Delete'])
def DisapproveCourse(request, id):
    blacklistLinks.objects.create(link=CourseToFilter.objects.get(id=id).url)
    CourseToFilter.objects.get(id=id).Disapprove()
    return Response({'message': 'Disapproved'})

@api_view(['Get'])
def getParsingReport(request):
    return Response({'ErrorNumber': ParsingError.objects.count(), 'ArtNumber': ArticleToFilter.objects.count(), 'ProjectNumber': ProjectToFilter.objects.count(), 'EventNumber': EventToFilter.objects.count(), 'CourseNumber': CourseToFilter.objects.count()})



