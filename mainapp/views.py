from datetime import datetime

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls.base import reverse_lazy
from django.utils.safestring import mark_safe
from django.views.generic.base import View, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from mainapp.models import News, Course, Lesson, CourseTeachers




class MainPageView(TemplateView):
    template_name = 'mainapp/index.html'


class NewsListView(ListView):
    model = News
    paginate_by = 5

    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)

class NewsCreateView(PermissionRequiredMixin, CreateView):
    model = News
    fields = "__all__"
    success_url = reverse_lazy("mainapp:news")
    permission_required = ("mainapp.add_news",)



class NewsDetailView(DetailView):
    model = News


class NewsUpdateView(PermissionRequiredMixin, UpdateView):
    model = News
    fields = "__all__"
    success_url = reverse_lazy("mainapp:news")
    permission_required = ("mainapp.change_news",)

class NewsDeleteView(PermissionRequiredMixin, DeleteView):
    model = News
    success_url = reverse_lazy("mainapp:news")
    permission_required = ("mainapp.delete_news",)

class CoursesPageView(TemplateView):
    template_name = 'mainapp/courses_list.html'


class CoursesListView(TemplateView):
    template_name = 'mainapp/courses_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.all()
        return context


class CoursesDetailView(TemplateView):
    template_name = "mainapp/courses_detail.html"

    def get_context_data(self, pk=None, **kwargs):
        context = super(CoursesDetailView, self).get_context_data(**kwargs)
        context["course_object"] = get_object_or_404(
            Course, pk=pk
        )
        context["lessons"] = Lesson.objects.filter(
            course=context["course_object"]
        )
        context["teachers"] = CourseTeachers.objects.filter(
            course=context["course_object"]
        )
        return context


class ContactsPageView(TemplateView):
    template_name = 'mainapp/contacts.html'


class DocSitePageView(TemplateView):
    template_name = 'mainapp/doc_site.html'


class LoginPageView(TemplateView):
    template_name = 'mainapp/../authapp/templates/authapp/login.html'

class SearchRedirectView(View):

    def get(self, request):
        query = request.GET.get('query', '')
        if query:
            return redirect(f"https://www.google.com/search?q={query}")
        else:
            return HttpResponse("No search query provided.")
