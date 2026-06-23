from django.urls import path, include
from rest_framework import routers

from .views import *

urlpatterns = [
    path('Articles/', ArticleApiView.as_view()),
    path('Projects/', ProjectApiView.as_view()),
    path('Courses/', CourseApiView.as_view()),
    path('Events/', EventApiView.as_view()),

    path('Articles/Sites/', getArticleSiteList),
    path('Projects/Sites/', getProjectSiteList),
    path('Courses/Sites/', getCourseSiteList),
    path('Events/Sites/', getEventSiteList),
]