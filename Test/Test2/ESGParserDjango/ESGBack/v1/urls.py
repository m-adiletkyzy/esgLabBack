from django.urls import path, include
from rest_framework import routers

from .views import *

urlpatterns = [
    path('Articles/', ArticleApiView.as_view()),
    path('Projects/', ProjectApiView.as_view()),
    path('Courses/', CourseApiView.as_view()),
    path('Events/', EventApiView.as_view()),

    path('OurArticles/<int:id>/', OurArticleApiView.as_view()),
    path('OurProjects/<int:id>/', OurProjectApiView.as_view()),
    path('OurCourses/<int:id>/', OurCourseApiView.as_view()),
    path('OurEvents/<int:id>/', OurEventApiView.as_view()),

    path('Articles/Sites/', getArticleSiteList),
    path('Projects/Sites/', getProjectSiteList),
    path('Courses/Sites/', getCourseSiteList),
    path('Events/Sites/', getEventSiteList),

    # For telegram bot
    path('ArticlesToFilter/', ArticlesToFilterApiView.as_view()),
    path('Approve/Article/<int:id>/', AproveArticle),
    path('Disapprove/Article/<int:id>/', DisapproveArticle),

    path('Errors/', getRecentParsingErrors.as_view()),
    path('Errors/<int:pk>/', ParsingErrorDetailView.as_view()),
    path('Report/', getParsingReport),
    path('RecentArticles/', RecentArticleApiView.as_view()),
    path('RecentOurArticles/', RecentOurArticlesApiView.as_view()),
    path('RecentOurProjects/', RecentOurProjectsApiView.as_view()),
    path('RecentOurCourses/', RecentOurСoursesApiView.as_view()),
    path('RecentOurEvents/', RecentOurEventsApiView.as_view()),
]