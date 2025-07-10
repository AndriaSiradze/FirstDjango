from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.http.response import JsonResponse
from django.template.loader import render_to_string
from django.views.generic.edit import CreateView
from django.utils.translation import gettext_lazy as _



class BaseModel(models.Model):
    """
    Base model for all models in the application.
    Contains common fields and methods.
    """

    created = models.DateTimeField(
        auto_now_add=True, verbose_name="Created", editable=False
    )
    updated = models.DateTimeField(
        auto_now=True, verbose_name="Edited", editable=False
    )
    deleted = models.BooleanField(default=False)

    def delete(self, *args):
        self.deleted = True
        self.save()

    class Meta:
        abstract = True


# Create your models here.
class News(BaseModel):
    title = models.CharField(max_length=256, verbose_name=_("Title"))
    preamble = models.CharField(max_length=1024, verbose_name=_("Preamble"))
    body = models.TextField(blank=True, null=True, verbose_name=_("Body"))
    body_as_markdown = models.BooleanField(
        default=False, verbose_name="As markdown"
    )

    def __str__(self) -> str:
        return f"{self.pk} {self.title}"

    # getting by decending pk
    class Meta:
        ordering = ("-pk",)
        verbose_name_plural = "News"
        verbose_name = "News"


class CoursesManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class Course(BaseModel):
    objects = CoursesManager()
    name = models.CharField(max_length=256, verbose_name=_("Name"))
    description = models.TextField(
        verbose_name=_("Description"), blank=True, null=True
    )
    description_as_markdown = models.BooleanField(
        verbose_name=_("As markdown"), default=False
    )
    cost = models.DecimalField(
        max_digits=8, decimal_places=2, verbose_name="Cost", default=0
    )
    cover = models.CharField(
        max_length=25, default="no_image.svg", verbose_name="Cover"
    )

    def __str__(self) -> str:
        return f"{self.pk} {self.name}"


class Lesson(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    num = models.PositiveIntegerField(verbose_name="Lesson number")
    title = models.CharField(max_length=256, verbose_name="Name")
    description = models.TextField(
        verbose_name="Description", blank=True, null=True
    )
    description_as_markdown = models.BooleanField(
        verbose_name="As markdown", default=False
    )

    class Meta:
        ordering = ("course", "num")


class CourseTeachers(BaseModel):
    course = models.ManyToManyField(Course)
    name_first = models.CharField(max_length=128, verbose_name="Name")
    name_second = models.CharField(max_length=128, verbose_name="Surname")
    day_birth = models.DateField(verbose_name="Birth date")

    def __str__(self) -> str:
        return "{0:0>3} {1} {2}".format(
            self.pk, self.name_second, self.name_first
        )


class CourseFeedback(models.Model):
    RATING = ((5, "⭐⭐⭐⭐⭐"), (4, "⭐⭐⭐⭐"), (3, "⭐⭐⭐"), (2, "⭐⭐"),
              (1, "⭐"))
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name=_("Course")
    )
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, verbose_name=_("User")
    )
    feedback = models.TextField(
        default=("No feedback"), verbose_name=_("Feedback")
    )
    rating = models.SmallIntegerField(
        choices=RATING, default=5, verbose_name="Rating"
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name="Created")
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.course} ({self.user})"

