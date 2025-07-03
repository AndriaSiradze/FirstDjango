from django.contrib import admin
from django.utils.translation import gettext_lazy as _

# Register your models here.
from mainapp import models as mainapp_models

# admin.site.register(mainapp_models.News)


@admin.register(mainapp_models.News)
class NewsAdmin(admin.ModelAdmin):
    search_fields = ['title', 'preamble', 'body']


@admin.register(mainapp_models.Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ["id", 'get_course_name',"num", "title", "deleted"]
    ordering = ["-course__name", "-num"]
    list_per_page = 2
    list_filter = ['course', 'deleted', 'created']
    actions = ['mark_deleted']
    def get_course_name(self, obj):
        return obj.course.name

    def mark_deleted(self, request, queryset):
        queryset.update(deleted=True)

    get_course_name.short_description = _("Course")
    mark_deleted.short_description = _("Mark deleted")

@admin.register(mainapp_models.Course)
class CourseAdmin(admin.ModelAdmin):
    pass