from typing import *

from django.conf import settings
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from .forms import LoginForm, SignUpForm


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
    template_name = "main/login.html"
    form_class = LoginForm
