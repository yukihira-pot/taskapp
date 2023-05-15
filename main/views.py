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
            print(form)
            if form.is_valid():
                form = form.save(commit=False)
                form.user = self.request.user
                form.save()
                return redirect("main:my_tasks")
            return redirect("main:my_tasks")

        elif "task-complete" in self.request.POST["name"]:
            complete_pk = int(self.request.POST.get("task-pk"))
            completed_task = Task.objects.get(pk=complete_pk)
            completed_task.is_completed = True
            completed_task.save()
            return JsonResponse({})
        
        elif "task-edit" in self.request.POST["name"]:
            # 編集できるようにする
            form_content = self.request.POST
            edit_pk = int(form_content.get("task-pk"))
            edit_task = Task.objects.get(pk=edit_pk)
            edit_task.title = form_content.get("title")
            edit_task.content = form_content.get("content")

            deadline_str = form_content.get("deadline_0") + " " + form_content.get("deadline_1")
            deadline_dt = timezone.make_aware(datetime.strptime(deadline_str, '%Y-%m-%d %H:%M'))
            edit_task.deadline = deadline_dt

            has_deadline, deadline_passed, deadline, remaining_datetime\
                 = self.deadline_preprocess(deadline_str)

            edit_task.save()
            return JsonResponse({
                "task-pk": form_content.get("task-pk"),
                "title": form_content.get("title"),
                "content": form_content.get("content"),
                "has_deadline": has_deadline,
                "deadline_passed": deadline_passed,
                "deadline": deadline,
                "remaining_datetime": remaining_datetime,
            })
        
    def deadline_preprocess(self, deadline_str: str):
        def elapsed_time(dt):
            has_deadline = True
            deadline_passed = False

            if not dt:
                has_deadline = False
                return has_deadline, None, None, None
            zero = timedelta()
            one_hour = timedelta(hours=1)
            one_day = timedelta(days=1)
            one_week = timedelta(days=7)
            two_weeks = timedelta(days=14)
            one_month = timedelta(days=30)

            if dt < zero:
                deadline_passed = True
                if -dt > one_day:
                    remaining_datetime = f"{-dt.days}日"
                elif -dt > one_hour:
                    remaining_datetime = f"{(-dt).seconds // 3600}時間{(-dt).seconds % 60}分"
                else:
                    remaining_datetime = f"{(-dt).seconds // 60}分"
            else:
                if dt < one_hour:  # 経過時間が 1 時間以内のとき
                    remaining_datetime = f"{dt.seconds // 60}分"
                elif dt < one_day:  # 経過時間が 1 日以内のとき
                    remaining_datetime = f"{dt.seconds // 3600}時間"
                elif dt < one_week:  # 経過時間が 1 週間以内のとき
                    remaining_datetime = f"{dt.days}日"
                elif dt < two_weeks:
                    remaining_datetime = f"1週間と{dt.days - 7}日"
                elif dt < one_month:
                    remaining_datetime = f"{dt.days}日"
                else:
                    remaining_datetime = f"{dt.days // 30}カ月と{dt.days % 30}日"
            return has_deadline, deadline_passed, remaining_datetime

        deadline_dt = timezone.make_aware(datetime.strptime(deadline_str, '%Y-%m-%d %H:%M'))
        # leading zero を消すために strftime を避ける
        deadline_str \
            = f"{deadline_dt.year}年{deadline_dt.month}月{deadline_dt.day}日{deadline_dt.hour}:{deadline_dt.minute}"
        has_deadline, deadline_passed, remaining_datetime = elapsed_time(deadline_dt - timezone.now())
        return \
            has_deadline, deadline_passed, deadline_str, remaining_datetime



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
