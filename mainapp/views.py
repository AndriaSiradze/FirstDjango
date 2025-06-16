from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View, TemplateView


# Create your views here.


class MainPageView(TemplateView):
    template_name = 'mainapp/index.html'

class NewsPageView(TemplateView):
    template_name = 'mainapp/news.html'

class CoursesPageView(TemplateView):
    template_name = 'mainapp/courses_list.html'

class ContactsPageView(TemplateView):
    template_name = 'mainapp/contacts.html'

class DocSitePageView(TemplateView):
    template_name = 'mainapp/doc_site.html'

class LoginPageView(TemplateView):
    template_name = 'mainapp/login.html'

