import os

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse_lazy
from django.utils.safestring import mark_safe
from django.views.generic.base import TemplateView
from django.utils.translation import gettext as _
from django.views.generic.edit import CreateView, UpdateView

from authapp import models
from authapp.forms import CustomUserCreationForm, CustomUserChangeForm


class CustomLoginView(LoginView):
    template_name = 'authapp/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        response = super().form_valid(form)
        message = _("Login success!<br>Hi, %(username)s") % {
            "username": self.request.user.get_full_name() or self.request.user.get_username()
        }
        messages.info(self.request, mark_safe(message))
        return response

    def get_success_url(self):
        return reverse_lazy('mainapp:main_page')

    def form_invalid(self, form):
        for _unused, msg in form.error_messages.items():
            messages.add_message(
                self.request,
                messages.WARNING,
                mark_safe(f"Something goes worng:<br>{msg}"),
            )
        return self.render_to_response(self.get_context_data(form=form))


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('authapp:login')

    def dispatch(self, request, *args, **kwargs):
        messages.info(self.request, _("See you later!"))
        return super().dispatch(request, *args, **kwargs)


class RegisterView(CreateView):
    model = get_user_model()
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('mainapp:index')


class ProfileEditView(UserPassesTestMixin, UpdateView):
    model = get_user_model()
    form_class = CustomUserChangeForm

    def test_func(self):
        return True if self.request.user.pk == self.kwargs.get("pk") else False

    def get_success_url(self):
        return reverse_lazy("authapp:profile_edit", args=[self.request.user.pk])
