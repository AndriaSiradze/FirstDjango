"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls.conf import path

from mainapp.apps import MainappConfig
from mainapp.views import MainPageView, NewsPageView, CoursesPageView, ContactsPageView, DocSitePageView, LoginPageView, \
    NewsWithPaginatorView, SearchRedirectView, NewsPageDetailView, CoursesListView, CoursesDetailView

app_name = MainappConfig.name

urlpatterns = [
    path('', MainPageView.as_view(), name='index'),
    path('news/', NewsPageView.as_view(), name='news'),
    path("news/<int:pk>/", NewsPageDetailView.as_view(), name="news_detail"),
    path("news/<int:page>/", NewsWithPaginatorView.as_view(),name="news_paginator"),
    path('contacts/', ContactsPageView.as_view(), name='contacts'),
    path('doc_site/', DocSitePageView.as_view(), name='doc_site'),
    path('login/', LoginPageView.as_view(), name='login'),
    path("search/", SearchRedirectView.as_view(), name="search"),
    path("courses/", CoursesListView.as_view(), name="courses"),
    path("courses/<int:pk>/",CoursesDetailView.as_view(),name="courses_detail",),
]
