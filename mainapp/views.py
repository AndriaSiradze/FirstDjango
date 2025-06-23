from datetime import datetime

from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django.views.generic.base import View, TemplateView


# Create your views here.


class MainPageView(TemplateView):
    template_name = 'mainapp/index.html'


class NewsPageView(TemplateView):
    template_name = 'mainapp/news.html'

    def get_context_data(self, **kwargs):
        # Get all previous data
        context = super().get_context_data(**kwargs)
        # Create your own data
        context["news_title"] = "Громкий новостной заголовок"
        context["news_preview"] = "Предварительное описание, которое заинтересует каждого"
        context["range"] = range(5)
        context["datetime_obj"] = datetime.now()
        return context


class NewsWithPaginatorView(NewsPageView):


    def get_context_data(self, page, **kwargs):
        context = super().get_context_data(page=page,**kwargs)
        context["page_num"] = page
        return context


class CoursesPageView(TemplateView):
    template_name = 'mainapp/courses_list.html'


class ContactsPageView(TemplateView):
    template_name = 'mainapp/contacts.html'


class DocSitePageView(TemplateView):
    template_name = 'mainapp/doc_site.html'


class LoginPageView(TemplateView):
    template_name = 'mainapp/login.html'

class SearchRedirectView(View):

    def get(self, request):
        query = request.GET.get('query', '')
        if query:
            return redirect(f"https://www.google.com/search?q={query}")
        else:
            return HttpResponse("No search query provided.")