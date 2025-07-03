import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse_lazy
from django.utils.safestring import mark_safe
from django.views.generic.base import TemplateView
from django.utils.translation import gettext as _
from authapp import models


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        response = super().form_valid(form)
        message = _("Login success!<br>Hi, %(username)s") % {
            "username": self.request.user.get_full_name() or self.request.user.get_username()
        }
        messages.info(self.request, mark_safe(message))
        return response

    def get_success_url(self):
        return reverse_lazy('mainapp:index')

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

class RegisterView(TemplateView):
    template_name = "registration/register.html"
    def post(self, request, *args, **kwargs):
        try:
            if all(
            (
            request.POST.get("username"),
            request.POST.get("email"),
            request.POST.get("password1"),
            request.POST.get("password1") == request.POST.get("password2"),
            )
        ):
                new_user = models.CustomUser.objects.create(
                username=request.POST.get("username"),
                first_name=request.POST.get("first_name"),
                last_name=request.POST.get("last_name"),
                age=request.POST.get("age")
                if request.POST.get("age")
                else 0,
                avatar=request.FILES.get("avatar"),
                email=request.POST.get("email"),
                )
                new_user.set_password(request.POST.get("password1"))
                new_user.save()
                messages.add_message(
                request, messages.INFO, _("Registration success!")
                )
                return HttpResponseRedirect(reverse_lazy("authapp:login"))
            else:
                messages.add_message(
                    request,
                    messages.WARNING,
                    _("Please fill all fields and make sure passwords match."),
                )

        except Exception as exp:
            print(exp)
            messages.add_message(
            request,
            messages.WARNING,
            mark_safe(f"Something goes worng:<br>{exp}"),
            )
            return HttpResponseRedirect(reverse_lazy("authapp:register"))


class ProfileEditView(LoginRequiredMixin, TemplateView):
    """Profile edit wie"""
    template_name = "registration/profile_edit.html"
    login_url = reverse_lazy("authapp:login")
    def post(self, request, *args, **kwargs):

        try:

            if request.POST.get("username"):
                request.user.username = request.POST.get("username")
            if request.POST.get("first_name"):
                request.user.first_name = request.POST.get("first_name")
            if request.POST.get("last_name"):
                request.user.last_name = request.POST.get("last_name")
            if request.POST.get("age"):
                request.user.age = request.POST.get("age")
            if request.POST.get("email"):
                request.user.email = request.POST.get("email")
            if request.FILES.get("avatar"):
                if request.user.avatar and os.path.exists(
                        request.user.avatar.path
                ):
                    os.remove(request.user.avatar.path)
            request.user.avatar = request.FILES.get("avatar")
            request.user.save()
            messages.add_message(request, messages.INFO, _("Saved!"))
        except Exception as exp:
            print(exp)
            messages.add_message(
                request,
                messages.WARNING,
                mark_safe(f"Something goes worng:<br>{exp}"),
            )
            return HttpResponseRedirect(reverse_lazy("authapp:profile_edit"))
