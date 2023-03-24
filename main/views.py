from typing import *

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import QuerySet
from django.shortcuts import HttpResponse, redirect, render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, FormView, ListView,
                                  TemplateView)
from django.views.generic.edit import ModelFormMixin

from .forms import LoginForm, SignUpForm, TaskCreationForm
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
        queryset = Task.objects.filter(user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = {
            "username": self.request.user.username,
            "form": TaskCreationForm,
            "my_tasks_list": self.get_queryset(),
            "user": self.request.user,
        }
        return context

    def post(self, request):
        form = TaskCreationForm(self.request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = self.request.user
            form.save()
            return redirect("main:my_tasks")
        return redirect("main:my_tasks")


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy("main:my_tasks")
    template_name = "main/task-delete-confirm.html"
