from typing import *
from django.utils import timezone
from datetime import timedelta, datetime
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import QuerySet, F, BooleanField, Case, When
from django.http import JsonResponse
from django.shortcuts import HttpResponse, redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    FormView,
    ListView,
    TemplateView,
    UpdateView,
)
from django.views.generic.edit import ModelFormMixin

from .forms import (
    EmailChangeForm,
    LoginForm,
    SignUpForm,
    TaskCreationForm,
    UsernameChangeForm,
)
from .models import Task


class IndexView(TemplateView):
    """インデックス画面を表示するためのビュー"""

    template_name = "main/index.html"


class SignUpView(CreateView):
    """会員登録用のビュー"""

    model = settings.AUTH_USER_MODEL
    form_class = SignUpForm
    success_url = reverse_lazy("main:my_tasks")
    template_name = "main/signup.html"


class MyLoginView(LoginView):
    """ログイン用のビュー"""

    template_name = "main/login.html"
    form_class = LoginForm


# インポートの順番に注意 (LoginRequiredMixin を先に書く必要がある)
class TaskListView(LoginRequiredMixin, ListView, ModelFormMixin):
    """自分のタスク一覧を取得するビュー"""

    model = Task
    context_object_name = "my_tasks_list"
    template_name = "main/my-tasks.html"

    def get_queryset(self) -> QuerySet[Any]:
        queryset = Task.objects.filter(user=self.request.user).annotate(
                remaining_datetime = F("deadline") - timezone.now(),
                is_deadline_passed=Case(
                    When(remaining_datetime__lt=timedelta(), then=True),
                    default=False,
                    output_field=BooleanField(),
                ),
            ).order_by("deadline")
        return queryset

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = {
            "username": self.request.user.username,
            "task_form": TaskCreationForm,
            "usernamechange_form": UsernameChangeForm(instance=self.request.user),
            "emailchange_form": EmailChangeForm(instance=self.request.user),
            "my_tasks_list": self.get_queryset(),
            "user": self.request.user,
        }
        return context

    def post(self, request):
        if not "name" in self.request.POST:
            form = TaskCreationForm(self.request.POST)
            if form.is_valid():
                form = form.save(commit=False)
                form.user = self.request.user
                form.save()
                return redirect("main:my_tasks")
            return redirect("main:my_tasks")
        elif "task-complete" in self.request.POST["name"]:
            delete_pk = int(self.request.POST.get("task-pk"))
            Task.objects.get(pk=delete_pk).delete()
            return JsonResponse({})


class UsernameUpdateView(LoginRequiredMixin, UpdateView):
    """ユーザー名変更をしたときのビュー"""

    model = settings.AUTH_USER_MODEL
    template_name = "main/username_change.html"
    form_class = UsernameChangeForm
    success_url = "main:my_tasks"


class EmailUpdateView(LoginRequiredMixin, UpdateView):
    """Eメール変更をしたときのビュー"""

    model = settings.AUTH_USER_MODEL
    template_name = "main/email_change.html"
    success_url = "main:my_tasks"
